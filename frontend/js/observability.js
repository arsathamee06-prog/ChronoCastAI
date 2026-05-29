/**
 * Observability Module - Monitoring and health
 */

async function loadObservability() {
    try {
        showLoading();
        
        // Fetch observability data
        const obsData = await apiCall('/observability/dashboard');
        
        if (obsData.data) {
            updateObservabilityDashboard(obsData.data);
        }
        
        // Initialize monitoring charts
        initializeMonitoringCharts();
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showNotification(`Failed to load observability: ${error.message}`, 'error');
    }
}

function updateObservabilityDashboard(data) {
    // API Status
    const apiStatusContent = document.getElementById('api-status-content');
    if (apiStatusContent && data.api_health) {
        apiStatusContent.innerHTML = `
            <p><strong>Status:</strong> ${data.api_health.status}</p>
            <p><strong>Success Rate:</strong> ${data.api_health.success_rate_percent.toFixed(2)}%</p>
            <p><strong>Avg Response Time:</strong> ${data.api_health.average_response_time_ms.toFixed(2)}ms</p>
        `;
    }
    
    // System Health
    const systemHealthContent = document.getElementById('system-health-content');
    if (systemHealthContent && data.system_health) {
        systemHealthContent.innerHTML = `
            <p><strong>CPU Usage:</strong> ${data.system_health.cpu_usage_percent.toFixed(2)}%</p>
            <p><strong>Memory Usage:</strong> ${data.system_health.memory_usage_percent.toFixed(2)}%</p>
            <p><strong>Disk Usage:</strong> ${data.system_health.disk_usage_percent.toFixed(2)}%</p>
        `;
    }
    
    // Prediction Logs
    const predLogsContent = document.getElementById('prediction-logs-content');
    if (predLogsContent && data.predictions) {
        predLogsContent.innerHTML = `
            <p><strong>Total Predictions:</strong> ${data.predictions.total_predictions}</p>
            <p><strong>Success Rate:</strong> ${data.predictions.success_rate.toFixed(2)}%</p>
            <p><strong>Avg Accuracy:</strong> ${data.predictions.average_accuracy.toFixed(2)}%</p>
        `;
    }
}

function initializeMonitoringCharts() {
    // API Response Time Chart
    const apiCtx = document.getElementById('api-response-chart');
    if (apiCtx) {
        new Chart(apiCtx, {
            type: 'line',
            data: {
                labels: Array.from({length: 20}, (_, i) => `${i*5}min`),
                datasets: [{
                    label: 'Response Time (ms)',
                    data: Array.from({length: 20}, () => Math.random() * 200 + 50),
                    borderColor: chartColors.info,
                    backgroundColor: 'rgba(79, 172, 254, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: '#b0b0b0'
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: {
                            color: '#b0b0b0'
                        },
                        grid: {
                            color: '#2a2635'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#b0b0b0'
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
    
    // System Resources Chart
    const resourcesCtx = document.getElementById('system-resources-chart');
    if (resourcesCtx) {
        new Chart(resourcesCtx, {
            type: 'line',
            data: {
                labels: Array.from({length: 20}, (_, i) => `${i*5}min`),
                datasets: [
                    {
                        label: 'CPU %',
                        data: Array.from({length: 20}, () => Math.random() * 60 + 20),
                        borderColor: chartColors.warning,
                        tension: 0.4
                    },
                    {
                        label: 'Memory %',
                        data: Array.from({length: 20}, () => Math.random() * 50 + 30),
                        borderColor: chartColors.success,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: '#b0b0b0'
                        }
                    }
                },
                scales: {
                    y: {
                        max: 100,
                        ticks: {
                            color: '#b0b0b0'
                        },
                        grid: {
                            color: '#2a2635'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#b0b0b0'
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
}
