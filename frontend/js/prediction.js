/**
 * Prediction Module - Forecast generation
 */

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('prediction-form')) {
        setupPredictionHandlers();
    }
});

function setupPredictionHandlers() {
    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', handlePrediction);
}

async function handlePrediction(e) {
    e.preventDefault();
    
    if (!appState.trainedModels) {
        showNotification('Please train models first', 'warning');
        navigateToPage('upload');
        return;
    }
    
    try {
        showLoading();
        
        const horizon = parseInt(document.getElementById('forecast-horizon').value);
        const confidence = parseFloat(document.getElementById('confidence-level').value);
        const modelPath = appState.trainedModels.best_model.path;
        
        const predictionResponse = await apiCall('/predict', 'POST', {
            model_path: modelPath,
            forecast_horizon: horizon
        });
        
        appState.currentForecast = predictionResponse.data;
        
        // Display results
        displayPredictionResults(predictionResponse.data);
        
        showNotification('Forecast generated successfully', 'success');
        hideLoading();
    } catch (error) {
        hideLoading();
        showNotification(`Prediction failed: ${error.message}`, 'error');
    }
}

function displayPredictionResults(data) {
    const resultDiv = document.getElementById('prediction-result');
    resultDiv.style.display = 'block';
    
    // Create forecast chart
    const ctx = document.getElementById('prediction-chart');
    if (ctx && ctx.chart) {
        ctx.chart.destroy();
    }
    
    const forecastChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: data.forecast.length}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'Forecast',
                data: data.forecast,
                borderColor: chartColors.success,
                backgroundColor: 'rgba(67, 233, 123, 0.1)',
                tension: 0.4,
                fill: true,
                borderWidth: 2
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
    ctx.chart = forecastChart;
    
    // Display forecast details
    const detailsDiv = document.getElementById('forecast-details');
    detailsDiv.innerHTML = `
        <h4>Model: ${data.model_name}</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px;">
            <div>
                <p style="color: #b0b0b0; font-size: 12px;">Accuracy</p>
                <p style="font-size: 24px; font-weight: bold; color: #43e97b;">${data.accuracy.toFixed(2)}%</p>
            </div>
            <div>
                <p style="color: #b0b0b0; font-size: 12px;">RMSE</p>
                <p style="font-size: 24px; font-weight: bold; color: #667eea;">${data.rmse.toFixed(4)}</p>
            </div>
            <div>
                <p style="color: #b0b0b0; font-size: 12px;">MAE</p>
                <p style="font-size: 24px; font-weight: bold; color: #4facfe;">${data.mae.toFixed(4)}</p>
            </div>
        </div>
    `;
}
