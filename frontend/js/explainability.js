/**
 * Explainability Module - XAI insights
 */

async function loadExplainability() {
    if (!appState.currentForecast) {
        showNotification('Please generate a forecast first', 'warning');
        return;
    }
    
    try {
        showLoading();
        
        // Placeholder explanations
        const explanations = {
            trend: {
                title: 'Trend Analysis',
                content: 'The data shows an upward trend with 2.5% weekly increase. Future values are expected to continue rising.'
            },
            seasonality: {
                title: 'Seasonality',
                content: 'Strong monthly seasonality detected (strength: 45%). Peak values occur in Q4, trough in Q2.'
            },
            volatility: {
                title: 'Volatility',
                content: 'Moderate volatility observed (σ = 3.2). Forecast volatility is lower than historical, indicating stabilization.'
            },
            anomalies: {
                title: 'Anomalies',
                content: 'Detected 3 anomalies in the dataset. All are within acceptable ranges. No major outliers found.'
            },
            importance: {
                title: 'Feature Importance',
                content: 'Recent trend (45%), Seasonality (35%), Volatility (20%). Model primarily relies on trend and seasonal patterns.'
            },
            confidence: {
                title: 'Confidence Interval',
                content: '95% confidence: Forecast range ±2.5% from predicted values. Wider intervals for longer horizons.'
            }
        };
        
        // Update explanations
        for (const [key, exp] of Object.entries(explanations)) {
            const element = document.getElementById(`${key}-explanation`);
            if (element) {
                element.innerHTML = `<p>${exp.content}</p>`;
            }
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showNotification(`Failed to load explanations: ${error.message}`, 'error');
    }
}
