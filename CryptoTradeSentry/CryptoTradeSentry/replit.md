# XEC Price Monitor

## Overview

The XEC Price Monitor is a Flask-based web application that monitors eCash (XEC) cryptocurrency prices in real-time and sends Telegram alerts when prices cross configured thresholds. The application features a web dashboard for monitoring current prices, viewing price history charts, and configuring alert settings.

## System Architecture

### Backend Framework
- **Flask**: Lightweight Python web framework serving as the main application server
- **SQLAlchemy**: ORM for database operations with declarative base model structure
- **Threading**: Background price monitoring runs in a separate daemon thread

### Frontend Technology
- **Bootstrap 5**: Dark theme UI framework for responsive design
- **Chart.js**: Real-time price charting library
- **Feather Icons**: Consistent iconography throughout the interface
- **Vanilla JavaScript**: Client-side functionality for real-time updates

### Database Design
- **PostgreSQL**: Production-grade database with improved performance and reliability
- **Connection Pooling**: Configured with pool recycling and pre-ping health checks
- **Automatic Schema Creation**: Tables created on application startup
- **Environment Variables**: Full PostgreSQL configuration via DATABASE_URL, PGPORT, PGUSER, PGPASSWORD, PGDATABASE, PGHOST

## Key Components

### Core Models
1. **MonitorConfig**: Stores Telegram bot configuration, price thresholds, and monitoring settings
2. **PriceAlert**: Logs all price alerts sent, including success/failure status
3. **PriceHistory**: Maintains historical price data for charting and analysis

### Service Classes
1. **PriceMonitor**: Main monitoring service that fetches prices from Binance API and manages alert logic
2. **TelegramService**: Handles Telegram bot integration for sending notifications

### Web Interface
1. **Dashboard**: Real-time price display, monitoring status, recent alerts, and price charts
2. **Settings**: Configuration interface for Telegram bot setup and threshold management

## Data Flow

1. **Price Monitoring Loop**:
   - Fetches XEC/USDT price from Binance API every 30 seconds (configurable)
   - Stores price data in PriceHistory table
   - Evaluates against configured upper/lower thresholds

2. **Alert System**:
   - Generates alerts when thresholds are breached
   - Sends notifications via Telegram bot
   - Logs alert attempts in PriceAlert table

3. **Web Dashboard**:
   - Displays current price and monitoring status
   - Shows recent alerts from last 24 hours
   - Renders interactive price chart with historical data

## External Dependencies

### APIs
- **CoinGecko API**: Primary data source for XEC/USDT price feeds (more reliable than Binance)
- **Telegram Bot API**: Message delivery system for price alerts

### Python Packages
- **Flask & Extensions**: Web framework and SQLAlchemy integration
- **Requests**: HTTP client for external API calls
- **Werkzeug**: WSGI utilities including proxy fix middleware

### Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme
- **Chart.js**: Real-time charting capability
- **Feather Icons**: Scalable vector icons

## Deployment Strategy

### Environment Configuration
- **SESSION_SECRET**: Flask session encryption key
- **DATABASE_URL**: Database connection string (defaults to SQLite)
- **Production Considerations**: ProxyFix middleware configured for reverse proxy deployment

### Application Structure
- **main.py**: Entry point that starts both web server and monitoring thread
- **app.py**: Application factory and configuration setup
- **Modular Design**: Separated concerns for routes, models, and services

### Monitoring Architecture
- **Background Threading**: Price monitoring runs independently of web requests
- **Graceful Degradation**: Web interface remains functional even if monitoring fails
- **Error Handling**: Comprehensive logging and error recovery throughout

## Deployment Strategy

The application is designed for cloud deployment with:
- Environment-based configuration
- Proxy-aware middleware
- Threaded background processing
- Persistent PostgreSQL storage for production reliability

## Changelog

```
Changelog:
- July 08, 2025. Initial setup
- July 08, 2025. Upgraded from SQLite to PostgreSQL database for improved performance and reliability
- July 08, 2025. Switched from Binance API to CoinGecko API for more reliable XEC/USDT price data
- July 08, 2025. Updated all UI references to consistently show XEC/USDT instead of XEC/USD
- July 08, 2025. Improved price fetching to use CoinGecko's Binance ticker endpoint for more accurate XEC/USDT pricing
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```