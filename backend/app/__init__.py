"""
Time Series AI Forecasting Platform - Flask Application Factory
"""
from flask import Flask, render_template
from flask_cors import CORS
import logging
import os
from app.config.settings import Config

def create_app(config_class=Config):
    """
    Application factory pattern for Flask
    """
    # Configure static files to serve from frontend directory
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'frontend')
    app = Flask(__name__, static_folder=frontend_path, static_url_path='/static', template_folder=frontend_path)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Serve frontend
    @app.route('/')
    def serve_index():
        return render_template('index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        from flask import send_from_directory
        if path.startswith('static/'):
            return send_from_directory(frontend_path, path[len('static/'):])
        if path.endswith('.html'):
            return render_template(path)
        if os.path.isfile(os.path.join(frontend_path, path)):
            return send_from_directory(frontend_path, path)
        return render_template('index.html')

    # Health check
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'Time Series AI'}, 200
    
    return app

def register_blueprints(app):
    """Register Flask blueprints"""
    from app.routes import api_bp, dashboard_bp, prediction_bp, model_bp, explainability_bp, observability_bp
    
    app.register_blueprint(api_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(model_bp)
    app.register_blueprint(explainability_bp)
    app.register_blueprint(observability_bp)

def register_error_handlers(app):
    """Register error handlers"""
    from app.utils.error_handler import handle_error
    
    @app.errorhandler(404)
    def not_found_error(error):
        return handle_error("Resource not found", 404)
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal error: {error}")
        return handle_error("Internal server error", 500)

def setup_logging(app):
    """Setup application logging"""
    import os
    from logging.handlers import RotatingFileHandler
    
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler('logs/timeseries_ai.log', maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Time Series AI Forecasting Platform startup')
