"""
Explainability Blueprint - XAI endpoints
"""
from flask import Blueprint, request, current_app
from app.utils.error_handler import success_response, handle_error
from app.ml.explainability.explainer import TimeSeriesExplainer
import numpy as np

explainability_bp = Blueprint('explainability', __name__, url_prefix='/api/explainability')

@explainability_bp.route('/explanation', methods=['POST'])
def get_explanation():
    """Get XAI explanation for forecast"""
    try:
        data = request.get_json()
        historical_data = np.array(data.get('historical_data', []))
        forecast_data = np.array(data.get('forecast_data', []))
        seasonal_period = data.get('seasonal_period', 12)
        
        if len(historical_data) == 0 or len(forecast_data) == 0:
            return handle_error("Historical and forecast data required", 400)
        
        # Generate explanation
        explainer = TimeSeriesExplainer(historical_data, forecast_data)
        explanation = explainer.comprehensive_explanation(seasonal_period)
        
        return success_response(
            data=explanation,
            message="Explanation generated successfully"
        )
    except Exception as e:
        return handle_error(str(e), 500)

@explainability_bp.route('/trend', methods=['POST'])
def analyze_trend():
    """Analyze trend in data"""
    try:
        data = request.get_json()
        historical_data = np.array(data.get('historical_data', []))
        
        explainer = TimeSeriesExplainer(historical_data, np.array([]))
        trend = explainer.trend_analysis()
        
        return success_response(
            data=trend,
            message="Trend analysis completed"
        )
    except Exception as e:
        return handle_error(str(e), 500)

@explainability_bp.route('/seasonality', methods=['POST'])
def analyze_seasonality():
    """Analyze seasonality in data"""
    try:
        data = request.get_json()
        historical_data = np.array(data.get('historical_data', []))
        seasonal_period = data.get('seasonal_period', 12)
        
        explainer = TimeSeriesExplainer(historical_data, np.array([]))
        seasonality = explainer.seasonality_analysis(seasonal_period)
        
        return success_response(
            data=seasonality,
            message="Seasonality analysis completed"
        )
    except Exception as e:
        return handle_error(str(e), 500)

@explainability_bp.route('/volatility', methods=['POST'])
def analyze_volatility():
    """Analyze volatility in data"""
    try:
        data = request.get_json()
        historical_data = np.array(data.get('historical_data', []))
        
        explainer = TimeSeriesExplainer(historical_data, np.array([]))
        volatility = explainer.volatility_analysis()
        
        return success_response(
            data=volatility,
            message="Volatility analysis completed"
        )
    except Exception as e:
        return handle_error(str(e), 500)

@explainability_bp.route('/anomalies', methods=['POST'])
def detect_anomalies():
    """Detect anomalies in data"""
    try:
        data = request.get_json()
        historical_data = np.array(data.get('historical_data', []))
        
        explainer = TimeSeriesExplainer(historical_data, np.array([]))
        anomalies = explainer.anomaly_detection()
        
        return success_response(
            data=anomalies,
            message="Anomaly detection completed"
        )
    except Exception as e:
        return handle_error(str(e), 500)
