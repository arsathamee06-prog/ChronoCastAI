"""
Routes module - Blueprint definitions
"""
from app.routes.api import api_bp
from app.routes.dashboard import dashboard_bp
from app.routes.prediction import prediction_bp
from app.routes.model import model_bp
from app.routes.explainability import explainability_bp
from app.routes.observability import observability_bp

__all__ = ['api_bp', 'dashboard_bp', 'prediction_bp', 'model_bp', 'explainability_bp', 'observability_bp']
