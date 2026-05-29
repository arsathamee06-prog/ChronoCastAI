/**
 * Main JavaScript - Application initialization and navigation
 */

const API_BASE_URL = 'http://localhost:5000/api';

// App State
const appState = {
    currentPage: 'dashboard',
    uploadedFile: null,
    processedData: null,
    trainedModels: null,
    currentForecast: null
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupNavigation();
    loadDashboard();
});

function initializeApp() {
    console.log('Initializing Time Series AI Platform...');
    setupEventListeners();
    
    // Load initial data
    checkAPIHealth();
}

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.dataset.page;
            navigateToPage(page);
        });
    });
}

function navigateToPage(pageName) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    
    // Remove active class from nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    
    // Show selected page
    const selectedPage = document.getElementById(`${pageName}-page`);
    if (selectedPage) {
        selectedPage.classList.add('active');
    }
    
    // Add active class to clicked nav link
    const clickedLink = document.querySelector(`[data-page="${pageName}"]`);
    if (clickedLink) {
        clickedLink.classList.add('active');
    }
    
    appState.currentPage = pageName;
    
    // Load page-specific content
    switch(pageName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'models':
            loadModels();
            break;
        case 'explainability':
            loadExplainability();
            break;
        case 'observability':
            loadObservability();
            break;
    }
}

function setupEventListeners() {
    // Global event listeners
    document.addEventListener('dragover', handleDragOver);
    document.addEventListener('drop', handleDrop);
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    // Handle file drop if on upload page
    if (appState.currentPage === 'upload') {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            document.getElementById('file-input').files = files;
        }
    }
}

// Utility Functions
function showLoading() {
    document.getElementById('loading-spinner').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-spinner').style.display = 'none';
}

function showNotification(message, type = 'success', duration = 3000) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification notification-${type}`;
    notification.style.display = 'block';
    
    setTimeout(() => {
        notification.style.display = 'none';
    }, duration);
}

async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('API Health:', data);
    } catch (error) {
        console.warn('API not available yet:', error);
    }
}

// Chart Colors
const chartColors = {
    primary: '#667eea',
    secondary: '#764ba2',
    success: '#43e97b',
    warning: '#f5576c',
    info: '#4facfe',
    danger: '#ff6b6b'
};

// Make API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'API error');
        }
        
        return result;
    } catch (error) {
        console.error('API Call Error:', error);
        showNotification(`Error: ${error.message}`, 'error');
        throw error;
    }
}

// Load Dashboard
async function loadDashboard() {
    try {
        showLoading();
        
        // Fetch dashboard data
        const dashboardData = await apiCall('/dashboard/overview');
        
        // Update metrics safely
        if (dashboardData.data) {
            const setMetric = (id, value) => {
                const element = document.getElementById(id);
                if (element) {
                    element.textContent = value;
                }
            };

            const activeModelsValue = Array.isArray(dashboardData.data.active_models)
                ? dashboardData.data.active_models.length
                : dashboardData.data.active_models || 'N/A';

            setMetric('best-accuracy', dashboardData.data.best_model_accuracy.toFixed(2) + '%');
            setMetric('total-predictions', dashboardData.data.total_predictions);
            setMetric('active-models', activeModelsValue);
            setMetric('system-health', dashboardData.data.system_health);
        }
        
        // Initialize charts with API-driven data
        await initializeDashboardCharts();
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showNotification('Failed to load dashboard', 'error');
        console.error('loadDashboard error', error);
    }
}

async function initializeDashboardCharts() {
    let modelComparisonData = null;
    let timeSeriesData = null;

    try {
        modelComparisonData = await apiCall('/dashboard/model-comparison');
    } catch (error) {
        console.warn('Model comparison fetch failed, using fallback data.', error);
    }

    try {
        timeSeriesData = await apiCall('/dashboard/time-series');
    } catch (error) {
        console.warn('Time series fetch failed, using fallback data.', error);
    }

    const safeChart = (ctx, config, name) => {
        try {
            const chart = new Chart(ctx, config);
            console.log(`Rendered ${name} chart`, chart);
            return chart;
        } catch (error) {
            console.error(`Chart render failed for ${name}:`, error);
            showNotification(`Chart render failed for ${name}`, 'error');
            return null;
        }
    };

    // Model Comparison Chart
    const modelCtx = document.getElementById('model-comparison-chart');
    if (modelCtx) {
        const comparison = modelComparisonData?.data?.models || {
            'Linear Regression': {accuracy: 78},
            'Moving Average': {accuracy: 72},
            'ARIMA': {accuracy: 85},
            'SARIMA': {accuracy: 87},
            'Prophet': {accuracy: 90},
            'LSTM': {accuracy: 88}
        };

        const labels = Object.keys(comparison);
        const values = labels.map(name => comparison[name].accuracy || 0);

        safeChart(modelCtx, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Accuracy (%)',
                    data: values,
                    backgroundColor: [
                        chartColors.primary,
                        chartColors.secondary,
                        chartColors.info,
                        chartColors.success,
                        chartColors.warning,
                        chartColors.danger
                    ],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
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
        }, 'Model Comparison');
    }
    
    // Forecast vs Actual Chart
    const forecastCtx = document.getElementById('forecast-chart');
    if (forecastCtx) {
        const labels = timeSeriesData?.data?.dates || Array.from({length: 30}, (_, i) => `Day ${i+1}`);
        const historical = timeSeriesData?.data?.historical || Array.from({length: 30}, () => Math.random() * 100 + 50);
        const forecast = timeSeriesData?.data?.forecast || Array.from({length: 30}, () => Math.random() * 100 + 60);
        const upper = timeSeriesData?.data?.confidence_upper || forecast.map(value => value + 5);
        const lower = timeSeriesData?.data?.confidence_lower || forecast.map(value => value - 5);

        safeChart(forecastCtx, {
            type: 'line',
            data: {
                labels,
                datasets: [
                    {
                        label: 'Historical',
                        data: historical,
                        borderColor: chartColors.primary,
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Forecast',
                        data: forecast,
                        borderColor: chartColors.success,
                        tension: 0.4
                    },
                    {
                        label: 'Confidence Upper',
                        data: upper,
                        borderColor: 'rgba(102, 126, 234, 0.2)',
                        borderDash: [5, 5],
                        tension: 0.4,
                        fill: false
                    },
                    {
                        label: 'Confidence Lower',
                        data: lower,
                        borderColor: 'rgba(102, 126, 234, 0.2)',
                        borderDash: [5, 5],
                        tension: 0.4,
                        fill: false
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
        }, 'Forecast vs Actual');
    }
    
    // Seasonal Patterns
    const seasonalCtx = document.getElementById('seasonal-chart');
    if (seasonalCtx) {
        const seasonalData = timeSeriesData?.data?.seasonal_pattern || {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            values: [65, 59, 90, 81, 56, 55, 40, 60, 75, 85, 78, 88]
        };

        safeChart(seasonalCtx, {
            type: 'radar',
            data: {
                labels: seasonalData.labels,
                datasets: [{
                    label: 'Seasonal Strength',
                    data: seasonalData.values,
                    borderColor: chartColors.primary,
                    backgroundColor: 'rgba(102, 126, 234, 0.2)'
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
                    r: {
                        ticks: {
                            color: '#b0b0b0'
                        },
                        grid: {
                            color: '#2a2635'
                        }
                    }
                }
            }
        }, 'Seasonal Patterns');
    }
    
    // Trend Analysis
    const trendCtx = document.getElementById('trend-chart');
    if (trendCtx) {
        const trendData = timeSeriesData?.data?.trend_analysis || {
            labels: Array.from({length: 30}, (_, i) => `Period ${i+1}`),
            values: Array.from({length: 30}, (_, i) => 50 + i * 0.5 + Math.random() * 10)
        };

        safeChart(trendCtx, {
            type: 'line',
            data: {
                labels: trendData.labels,
                datasets: [{
                    label: 'Trend',
                    data: trendData.values,
                    borderColor: chartColors.warning,
                    tension: 0.3
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
                            color: '#b0b0b0',
                            maxTicksLimit: 10
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        }, 'Trend Analysis');
    }
}

// Load Models
async function loadModels() {
    try {
        showLoading();
        
        const modelsData = await apiCall('/model/list');
        const grid = document.getElementById('models-grid');
        grid.innerHTML = '';
        
        if (modelsData.data && modelsData.data.models) {
            modelsData.data.models.forEach(model => {
                const card = createModelCard(model);
                grid.appendChild(card);
            });
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showNotification('Failed to load models', 'error');
    }
}

function createModelCard(modelName) {
    const card = document.createElement('div');
    card.className = 'model-card';
    card.innerHTML = `
        <div class="model-name">${modelName}</div>
        <div class="model-metrics">
            <div class="metric-item">
                <span class="metric-label">Accuracy</span>
                <span class="metric-value">--</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">RMSE</span>
                <span class="metric-value">--</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">MAE</span>
                <span class="metric-value">--</span>
            </div>
        </div>
    `;
    return card;
}

// Load Explainability
async function loadExplainability() {
    // Placeholder - will be implemented in explainability.js
}

// Load Observability
async function loadObservability() {
    // Placeholder - will be implemented in observability.js
}

console.log('Main.js loaded successfully');
