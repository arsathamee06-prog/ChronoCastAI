"""
Observability Blueprint - Monitoring endpoints
"""
from flask import Blueprint, current_app
from app.utils.error_handler import success_response, handle_error
from app.observability.monitor import APIMonitor, SystemHealthMonitor, ModelPerformanceTracker, PredictionLogger

observability_bp = Blueprint('observability', __name__, url_prefix='/api/observability')

# Initialize monitors
api_monitor = APIMonitor()
health_monitor = SystemHealthMonitor()
performance_tracker = ModelPerformanceTracker()
prediction_logger = PredictionLogger()

@observability_bp.route('/api-status', methods=['GET'])
def get_api_status():
    """Get API status and health"""
    try:
        status = api_monitor.get_health_status()
        uptime = api_monitor.get_uptime()
        stats = api_monitor.get_api_stats()
        
        return success_response(
            data={
                'api_status': status,
                'uptime': uptime,
                'statistics': stats
            },
            message="API status retrieved"
        )
    except Exception as e:
        return handle_error(str(e), 500)

@observability_bp.route('/system-health', methods=['GET'])
def get_system_health():
    """Get system health metrics"""
    try:
        current_status = health_monitor.get_system_status()
        average_health = health_monitor.get_average_health()
        
        return success_response(
            data={
                'current_status': current_status,
                'average_health': average_health
            },
            message="System health retrieved"
        )
    except Exception as e:
        return handle_error(str(e), 500)

@observability_bp.route('/model-performance', methods=['GET'])
def get_model_performance():
    """Get model performance metrics"""
    try:
        all_comparisons = performance_tracker.get_all_model_comparison()
        
        return success_response(
            data={'model_performance': all_comparisons},
            message="Model performance retrieved"
        )
    except Exception as e:
        return handle_error(str(e), 500)

@observability_bp.route('/prediction-logs', methods=['GET'])
def get_prediction_logs():
    """Get prediction logs"""
    try:
        limit = 100
        recent = prediction_logger.get_recent_predictions(limit)
        stats = prediction_logger.get_prediction_statistics()
        
        return success_response(
            data={
                'recent_predictions': recent,
                'statistics': stats
            },
            message="Prediction logs retrieved"
        )
    except Exception as e:
        return handle_error(str(e), 500)

@observability_bp.route('/dashboard', methods=['GET'])
def get_observability_dashboard():
    """Get complete observability dashboard"""
    try:
        api_health = api_monitor.get_health_status()
        system_health = health_monitor.get_system_status()
        predictions_stats = prediction_logger.get_prediction_statistics()
        
        return success_response(
            data={
                'api_health': api_health,
                'system_health': system_health,
                'predictions': predictions_stats,
                'timestamp': api_monitor.get_uptime()['start_time']
            },
            message="Observability dashboard retrieved"
        )
    except Exception as e:
        return handle_error(str(e), 500)
