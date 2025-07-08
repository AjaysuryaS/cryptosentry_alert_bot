// Dashboard JavaScript for real-time updates and chart management
class Dashboard {
    constructor() {
        this.chart = null;
        this.updateInterval = null;
        this.initChart();
        this.startRealTimeUpdates();
    }

    initChart() {
        const ctx = document.getElementById('priceChart');
        if (!ctx) return;

        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'XEC/USDT Price',
                    data: [],
                    borderColor: 'var(--bs-primary)',
                    backgroundColor: 'var(--bs-primary)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Time'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Price (USDT)'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toFixed(8);
                            }
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                elements: {
                    point: {
                        radius: 2,
                        hoverRadius: 5
                    }
                }
            }
        });

        // Load initial chart data
        this.loadChartData();
    }

    async loadChartData() {
        try {
            const response = await fetch('/api/price_history');
            const data = await response.json();
            
            if (data.length > 0) {
                const labels = data.map(item => {
                    const date = new Date(item.timestamp);
                    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                });
                const prices = data.map(item => item.price);
                
                this.chart.data.labels = labels;
                this.chart.data.datasets[0].data = prices;
                this.chart.update('none');
            }
        } catch (error) {
            console.error('Error loading chart data:', error);
        }
    }

    async updateCurrentPrice() {
        try {
            const response = await fetch('/api/current_price');
            const data = await response.json();
            
            // Update current price display
            const priceElement = document.getElementById('current-price');
            if (priceElement) {
                priceElement.textContent = `${data.price.toFixed(8)} USDT`;
                
                // Add price change animation
                priceElement.classList.add('price-updated');
                setTimeout(() => {
                    priceElement.classList.remove('price-updated');
                }, 1000);
            }
            
            // Update timestamp
            const timeElement = document.getElementById('update-time');
            if (timeElement) {
                timeElement.textContent = 'Just now';
            }
            
            // Update chart with new data point
            if (this.chart && data.timestamp) {
                const date = new Date(data.timestamp);
                const timeLabel = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                
                // Add new data point
                this.chart.data.labels.push(timeLabel);
                this.chart.data.datasets[0].data.push(data.price);
                
                // Keep only last 100 data points
                if (this.chart.data.labels.length > 100) {
                    this.chart.data.labels.shift();
                    this.chart.data.datasets[0].data.shift();
                }
                
                this.chart.update('none');
            }
            
        } catch (error) {
            console.error('Error updating current price:', error);
        }
    }

    startRealTimeUpdates() {
        // Update every 10 seconds
        this.updateInterval = setInterval(() => {
            this.updateCurrentPrice();
        }, 10000);
        
        // Initial update
        this.updateCurrentPrice();
    }

    stopRealTimeUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    const dashboard = new Dashboard();
    
    // Replace Feather icons
    feather.replace();
    
    // Handle page visibility changes to pause/resume updates
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            dashboard.stopRealTimeUpdates();
        } else {
            dashboard.startRealTimeUpdates();
        }
    });
});

// Utility function to format time ago
function timeAgo(date) {
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    
    const diffDays = Math.floor(diffHours / 24);
    return `${diffDays}d ago`;
}
