from flask import render_template, request, flash, redirect, url_for, jsonify
from app import app, db
from models import MonitorConfig, PriceAlert, PriceHistory
from datetime import datetime, timedelta
import logging

@app.route('/')
def dashboard():
    """Main dashboard showing current price and monitoring status"""
    config = MonitorConfig.query.first()
    
    # Get latest price
    latest_price = PriceHistory.query.order_by(PriceHistory.timestamp.desc()).first()
    current_price = latest_price.price if latest_price else 0.0
    
    # Get recent alerts (last 24 hours)
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_alerts = PriceAlert.query.filter(
        PriceAlert.created_at >= yesterday
    ).order_by(PriceAlert.created_at.desc()).limit(10).all()
    
    # Get price history for chart (last 24 hours)
    price_data = PriceHistory.query.filter(
        PriceHistory.timestamp >= yesterday
    ).order_by(PriceHistory.timestamp.asc()).all()
    
    return render_template('dashboard.html', 
                         config=config,
                         current_price=current_price,
                         recent_alerts=recent_alerts,
                         price_data=price_data)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Configuration page for monitoring settings"""
    config = MonitorConfig.query.first()
    
    if request.method == 'POST':
        bot_token = request.form.get('bot_token', '').strip()
        chat_id = request.form.get('chat_id', '').strip()
        upper_threshold = float(request.form.get('upper_threshold', 0.00001845))
        lower_threshold = float(request.form.get('lower_threshold', 0.00001830))
        check_interval = int(request.form.get('check_interval', 30))
        monitoring_enabled = 'monitoring_enabled' in request.form
        
        if not bot_token or not chat_id:
            flash('Bot Token and Chat ID are required!', 'error')
        elif upper_threshold <= lower_threshold:
            flash('Upper threshold must be greater than lower threshold!', 'error')
        else:
            if config:
                config.bot_token = bot_token
                config.chat_id = chat_id
                config.upper_threshold = upper_threshold
                config.lower_threshold = lower_threshold
                config.check_interval = check_interval
                config.monitoring_enabled = monitoring_enabled
                config.updated_at = datetime.utcnow()
            else:
                config = MonitorConfig(
                    bot_token=bot_token,
                    chat_id=chat_id,
                    upper_threshold=upper_threshold,
                    lower_threshold=lower_threshold,
                    check_interval=check_interval,
                    monitoring_enabled=monitoring_enabled
                )
                db.session.add(config)
            
            db.session.commit()
            flash('Settings saved successfully!', 'success')
            
            # Update monitor configuration
            try:
                from price_monitor import PriceMonitor
                # Get the running monitor instance if it exists
                import threading
                for thread in threading.enumerate():
                    if hasattr(thread, 'target') and thread.target and hasattr(thread.target, '__self__'):
                        if isinstance(thread.target.__self__, PriceMonitor):
                            thread.target.__self__.update_config()
                            break
            except Exception as e:
                logging.warning(f"Could not update monitor config: {e}")
            
            return redirect(url_for('dashboard'))
    
    return render_template('settings.html', config=config)

@app.route('/api/current_price')
def api_current_price():
    """API endpoint to get current price"""
    latest_price = PriceHistory.query.order_by(PriceHistory.timestamp.desc()).first()
    config = MonitorConfig.query.first()
    
    return jsonify({
        'price': latest_price.price if latest_price else 0.0,
        'timestamp': latest_price.timestamp.isoformat() if latest_price else None,
        'monitoring_enabled': config.monitoring_enabled if config else False,
        'upper_threshold': config.upper_threshold if config else 0.0,
        'lower_threshold': config.lower_threshold if config else 0.0
    })

@app.route('/api/price_history')
def api_price_history():
    """API endpoint to get price history for chart"""
    hours = request.args.get('hours', 24, type=int)
    since = datetime.utcnow() - timedelta(hours=hours)
    
    price_data = PriceHistory.query.filter(
        PriceHistory.timestamp >= since
    ).order_by(PriceHistory.timestamp.asc()).all()
    
    return jsonify([{
        'timestamp': p.timestamp.isoformat(),
        'price': p.price
    } for p in price_data])

@app.route('/toggle_monitoring', methods=['POST'])
def toggle_monitoring():
    """Toggle monitoring on/off"""
    config = MonitorConfig.query.first()
    if config:
        config.monitoring_enabled = not config.monitoring_enabled
        config.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Update monitor configuration
        try:
            from price_monitor import PriceMonitor
            # Get the running monitor instance if it exists
            import threading
            for thread in threading.enumerate():
                if hasattr(thread, 'target') and thread.target and hasattr(thread.target, '__self__'):
                    if isinstance(thread.target.__self__, PriceMonitor):
                        thread.target.__self__.update_config()
                        break
        except Exception as e:
            logging.warning(f"Could not update monitor config: {e}")
        
        status = "enabled" if config.monitoring_enabled else "disabled"
        flash(f'Monitoring {status}!', 'success')
    else:
        flash('Please configure settings first!', 'error')
    
    return redirect(url_for('dashboard'))
