"""
Flask configuration settings
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # CORS
    CORS_HEADERS = 'Content-Type'
    
    # API
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # ML/AI
    MODEL_SAVE_PATH = './models'
    DATA_UPLOAD_PATH = './data'
    MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB
    
    # Forecasting
    DEFAULT_FORECAST_HORIZON = 30  # days
    TEST_SIZE = 0.2
    VALIDATION_SIZE = 0.1
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///timeseries.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/timeseries_ai.log'
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
