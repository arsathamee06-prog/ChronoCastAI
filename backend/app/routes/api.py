"""
API Blueprint - Core forecasting endpoints
"""
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from app.utils.error_handler import success_response, handle_error
from app.utils.validators import validate_csv_file
from app.ml.preprocessing.preprocessor import TimeSeriesPreprocessor
from app.services.model_trainer import ModelTrainer
from app.observability.monitor import APIMonitor, PredictionLogger
import os
import time

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize monitors
api_monitor = APIMonitor()
prediction_logger = PredictionLogger()

@api_bp.before_request
def before_request():
    """Log request start time"""
    request.start_time = time.time()

@api_bp.after_request
def after_request(response):
    """Log API call"""
    if hasattr(request, 'start_time'):
        response_time = (time.time() - request.start_time) * 1000
        api_monitor.log_api_call(
            endpoint=request.endpoint or 'unknown',
            method=request.method,
            status_code=response.status_code,
            response_time=response_time
        )
    return response

@api_bp.route('/upload', methods=['POST'])
def upload_data():
    """Upload CSV data for forecasting"""
    try:
        if 'file' not in request.files:
            return handle_error("No file provided", 400)
        
        file = request.files['file']
        
        # Validate file
        is_valid, result = validate_csv_file(file)
        if not is_valid:
            return handle_error(result, 400)
        
        df = result
        
        # Save file
        filename = secure_filename(file.filename)
        data_path = current_app.config['DATA_UPLOAD_PATH']
        os.makedirs(data_path, exist_ok=True)
        filepath = os.path.join(data_path, filename)
        df.to_csv(filepath, index=False)
        
        return success_response(
            data={
                'filename': filename,
                'filepath': filepath,
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'rows': len(df),
                'columns_info': {col: str(df[col].dtype) for col in df.columns}
            },
            message="File uploaded successfully"
        )
    
    except Exception as e:
        current_app.logger.error(f"Upload error: {str(e)}")
        prediction_logger.log_error('data_upload', str(e))
        return handle_error(f"Upload failed: {str(e)}", 500)

@api_bp.route('/preprocess', methods=['POST'])
def preprocess_data():
    """Preprocess data"""
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        date_column = data.get('date_column')
        target_column = data.get('target_column')
        
        if not filepath:
            return handle_error("Filepath required", 400)
        
        # Load data
        import pandas as pd
        df = pd.read_csv(filepath)
        
        # Preprocess
        preprocessor = TimeSeriesPreprocessor(df, date_column, target_column)
        processed_df, info = preprocessor.preprocess(normalize=True, create_features_flag=True)
        
        # Save processed data
        processed_path = filepath.replace('.csv', '_processed.csv')
        processed_df.to_csv(processed_path)
        
        return success_response(
            data={
                'processed_filepath': processed_path,
                'shape': processed_df.shape,
                'date_column': info['date_column'],
                'target_column': info['target_column'],
                'seasonal_period': info['seasonal_period'],
                'columns': info['columns']
            },
            message="Data preprocessed successfully"
        )
    
    except Exception as e:
        current_app.logger.error(f"Preprocessing error: {str(e)}")
        prediction_logger.log_error('preprocessing', str(e))
        return handle_error(f"Preprocessing failed: {str(e)}", 500)

@api_bp.route('/train', methods=['POST'])
def train_models():
    """Train all forecasting models"""
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        processed_filepath = data.get('processed_filepath')
        target_column = data.get('target_column')
        seasonal_period = data.get('seasonal_period', 12)
        test_size = data.get('test_size', 0.2)
        validation_size = data.get('validation_size', 0.1)
        
        if not processed_filepath:
            return handle_error("Processed filepath required", 400)
        
        # Load processed data
        import pandas as pd
        df = pd.read_csv(processed_filepath, index_col=0, parse_dates=True)
        
        # Split data
        n = len(df)
        train_size = int(n * (1 - test_size - validation_size))
        val_size = int(n * validation_size)
        
        train_df = df[:train_size]
        val_df = df[train_size:train_size + val_size]
        
        # Train models
        trainer = ModelTrainer(current_app.config['MODEL_SAVE_PATH'])
        trainer.preprocessing_info = {
            'target_column': target_column,
            'seasonal_period': seasonal_period,
            'data_shape': df.shape
        }
        
        results = trainer.train_all_models(train_df, val_df, target_column, seasonal_period)
        
        # Select best model
        best_model_name, _, best_metrics = trainer.select_best_model()
        
        # Save models
        model_path = trainer.save_best_model()
        all_models = trainer.save_all_models()
        
        return success_response(
            data={
                'training_results': results,
                'best_model': {
                    'name': best_model_name,
                    'metrics': best_metrics,
                    'path': model_path
                },
                'all_models': all_models,
                'model_comparison': trainer.get_model_comparison()
            },
            message="Models trained successfully"
        )
    
    except Exception as e:
        current_app.logger.error(f"Training error: {str(e)}")
        prediction_logger.log_error('model_training', str(e))
        return handle_error(f"Training failed: {str(e)}", 500)

@api_bp.route('/predict', methods=['POST'])
def predict():
    """Make predictions using best model"""
    try:
        data = request.get_json()
        model_path = data.get('model_path')
        forecast_horizon = data.get('forecast_horizon', 30)
        
        if not model_path:
            return handle_error("Model path required", 400)
        
        # Load model
        import pickle
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        model = model_data['model']
        metrics = model_data['metrics']
        
        # Make forecast
        forecast = model.forecast(steps=forecast_horizon)
        
        # Log prediction
        prediction_logger.log_prediction(
            model_name=model_data['name'],
            input_data={'shape': model_data.get('preprocessing_info', {}).get('data_shape')},
            forecast=forecast.tolist(),
            accuracy=metrics.get('accuracy', 0),
            confidence=0.95
        )
        
        return success_response(
            data={
                'model_name': model_data['name'],
                'forecast': forecast.tolist(),
                'forecast_horizon': forecast_horizon,
                'accuracy': metrics.get('accuracy', 0),
                'rmse': metrics.get('rmse', 0),
                'mae': metrics.get('mae', 0)
            },
            message="Prediction generated successfully"
        )
    
    except Exception as e:
        current_app.logger.error(f"Prediction error: {str(e)}")
        prediction_logger.log_error('prediction', str(e))
        return handle_error(f"Prediction failed: {str(e)}", 500)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return success_response(
        data={'status': 'healthy', 'timestamp': time.time()},
        message="API is operational"
    )
