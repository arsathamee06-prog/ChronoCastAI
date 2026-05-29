"""
Model Training and Comparison Service
Trains multiple forecasting models and selects the best one
"""
import pickle
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from pathlib import Path
from datetime import datetime
from app.ml.models.forecasters import (
    LinearRegressionForecaster, MovingAverageForecaster, 
    ARIMAForecaster, SARIMAForecaster, ProphetForecaster, LSTMForecaster
)
from app.utils.logger import get_logger

logger = get_logger(__name__)

class ModelTrainer:
    """Train and compare multiple forecasting models"""
    
    def __init__(self, model_path: str = './models'):
        self.model_path = Path(model_path)
        self.model_path.mkdir(exist_ok=True)
        self.trained_models = {}
        self.model_performance = {}
        self.best_model_name = None
        self.best_model = None
        self.preprocessing_info = {}
    
    def train_all_models(self, train_df: pd.DataFrame, val_df: pd.DataFrame, 
                        target_column: str, seasonal_period: int = 12) -> Dict[str, Dict]:
        """
        Train all available forecasting models
        
        Args:
            train_df: Training data
            val_df: Validation data
            target_column: Target column name
            seasonal_period: Seasonal period for SARIMA
        
        Returns:
            Dictionary with training results for each model
        """
        results = {}
        
        # Prepare data
        X_train = np.arange(len(train_df)).reshape(-1, 1)
        y_train = train_df[target_column].values
        X_val = np.arange(len(train_df), len(train_df) + len(val_df)).reshape(-1, 1)
        y_val = val_df[target_column].values
        
        # 1. Linear Regression
        logger.info("Training Linear Regression...")
        try:
            lr_model = LinearRegressionForecaster()
            lr_model.fit(X_train, y_train)
            y_pred_val = lr_model.predict(X_val)
            metrics = lr_model.evaluate(y_val, y_pred_val)
            self.trained_models['Linear Regression'] = lr_model
            self.model_performance['Linear Regression'] = metrics
            results['Linear Regression'] = {'status': 'success', 'metrics': metrics}
            logger.info(f"Linear Regression trained: {metrics['accuracy']:.2f}%")
        except Exception as e:
            logger.error(f"Linear Regression training failed: {str(e)}")
            results['Linear Regression'] = {'status': 'failed', 'error': str(e)}
        
        # 2. Moving Average
        logger.info("Training Moving Average...")
        try:
            ma_model = MovingAverageForecaster(window=7)
            ma_model.fit(X_train, y_train)
            y_pred_val = ma_model.predict(np.arange(len(train_df) + len(val_df)).reshape(-1, 1))[-len(val_df):]
            metrics = ma_model.evaluate(y_val, y_pred_val)
            self.trained_models['Moving Average'] = ma_model
            self.model_performance['Moving Average'] = metrics
            results['Moving Average'] = {'status': 'success', 'metrics': metrics}
            logger.info(f"Moving Average trained: {metrics['accuracy']:.2f}%")
        except Exception as e:
            logger.error(f"Moving Average training failed: {str(e)}")
            results['Moving Average'] = {'status': 'failed', 'error': str(e)}
        
        # 3. ARIMA
        logger.info("Training ARIMA...")
        try:
            arima_model = ARIMAForecaster(order=(1, 1, 1))
            arima_model.fit(X_train, y_train)
            y_pred_val = arima_model.predict(X_val)
            metrics = arima_model.evaluate(y_val, y_pred_val[:len(y_val)])
            self.trained_models['ARIMA'] = arima_model
            self.model_performance['ARIMA'] = metrics
            results['ARIMA'] = {'status': 'success', 'metrics': metrics}
            logger.info(f"ARIMA trained: {metrics['accuracy']:.2f}%")
        except Exception as e:
            logger.error(f"ARIMA training failed: {str(e)}")
            results['ARIMA'] = {'status': 'failed', 'error': str(e)}
        
        # 4. SARIMA
        logger.info("Training SARIMA...")
        try:
            sarima_model = SARIMAForecaster(order=(1, 1, 1), seasonal_order=(1, 1, 1, max(seasonal_period, 12)))
            sarima_model.fit(X_train, y_train)
            y_pred_val = sarima_model.predict(X_val)
            metrics = sarima_model.evaluate(y_val, y_pred_val[:len(y_val)])
            self.trained_models['SARIMA'] = sarima_model
            self.model_performance['SARIMA'] = metrics
            results['SARIMA'] = {'status': 'success', 'metrics': metrics}
            logger.info(f"SARIMA trained: {metrics['accuracy']:.2f}%")
        except Exception as e:
            logger.error(f"SARIMA training failed: {str(e)}")
            results['SARIMA'] = {'status': 'failed', 'error': str(e)}
        
        # 5. Prophet
        logger.info("Training Prophet...")
        try:
            prophet_model = ProphetForecaster()
            dates = pd.date_range(start='2020-01-01', periods=len(train_df), freq='D')
            prophet_model.fit(X_train, y_train, dates=dates)
            y_pred_val = prophet_model.predict(X_val)
            if len(y_pred_val) >= len(y_val):
                y_pred_val = y_pred_val[:len(y_val)]
            metrics = prophet_model.evaluate(y_val, y_pred_val)
            self.trained_models['Prophet'] = prophet_model
            self.model_performance['Prophet'] = metrics
            results['Prophet'] = {'status': 'success', 'metrics': metrics}
            logger.info(f"Prophet trained: {metrics['accuracy']:.2f}%")
        except Exception as e:
            logger.error(f"Prophet training failed: {str(e)}")
            results['Prophet'] = {'status': 'failed', 'error': str(e)}
        
        # 6. LSTM
        logger.info("Training LSTM...")
        try:
            lstm_model = LSTMForecaster(lookback=10, epochs=30)
            lstm_model.fit(X_train, y_train)
            y_pred_val = lstm_model.predict(X_val)
            if len(y_pred_val) >= len(y_val):
                y_pred_val = y_pred_val[:len(y_val)]
            metrics = lstm_model.evaluate(y_val, y_pred_val)
            self.trained_models['LSTM'] = lstm_model
            self.model_performance['LSTM'] = metrics
            results['LSTM'] = {'status': 'success', 'metrics': metrics}
            logger.info(f"LSTM trained: {metrics['accuracy']:.2f}%")
        except Exception as e:
            logger.error(f"LSTM training failed: {str(e)}")
            results['LSTM'] = {'status': 'failed', 'error': str(e)}
        
        return results
    
    def select_best_model(self) -> Tuple[str, Any, Dict]:
        """
        Select the best performing model based on accuracy
        
        Returns:
            Tuple of (model_name, model_instance, metrics)
        """
        if not self.model_performance:
            raise ValueError("No models have been trained yet")
        
        # Sort by accuracy
        best_model_name = max(self.model_performance.keys(), 
                             key=lambda x: self.model_performance[x]['accuracy'])
        
        self.best_model_name = best_model_name
        self.best_model = self.trained_models[best_model_name]
        
        logger.info(f"Best model selected: {best_model_name} with {self.model_performance[best_model_name]['accuracy']:.2f}% accuracy")
        
        return best_model_name, self.best_model, self.model_performance[best_model_name]
    
    def save_best_model(self, filename: str = None) -> str:
        """
        Save the best model as a pickle file
        
        Args:
            filename: Filename for the model (default: best_model_<timestamp>.pkl)
        
        Returns:
            Path to the saved model
        """
        if self.best_model is None:
            raise ValueError("No best model selected yet")
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'best_model_{timestamp}.pkl'
        
        filepath = self.model_path / filename
        
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.best_model,
                'name': self.best_model_name,
                'metrics': self.model_performance[self.best_model_name],
                'preprocessing_info': self.preprocessing_info,
                'timestamp': datetime.now().isoformat()
            }, f)
        
        logger.info(f"Best model saved to {filepath}")
        return str(filepath)
    
    def save_all_models(self) -> Dict[str, str]:
        """
        Save all trained models
        
        Returns:
            Dictionary mapping model names to file paths
        """
        saved_paths = {}
        
        for model_name, model in self.trained_models.items():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{model_name.lower().replace(" ", "_")}_{timestamp}.pkl'
            filepath = self.model_path / filename
            
            with open(filepath, 'wb') as f:
                pickle.dump({
                    'model': model,
                    'name': model_name,
                    'metrics': self.model_performance.get(model_name, {}),
                    'timestamp': datetime.now().isoformat()
                }, f)
            
            saved_paths[model_name] = str(filepath)
            logger.info(f"Model {model_name} saved to {filepath}")
        
        return saved_paths
    
    def load_model(self, filepath: str) -> Tuple[Any, str, Dict]:
        """
        Load a saved model
        
        Args:
            filepath: Path to the saved model
        
        Returns:
            Tuple of (model, model_name, metrics)
        """
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        logger.info(f"Model {data['name']} loaded from {filepath}")
        return data['model'], data['name'], data['metrics']
    
    def get_model_comparison(self) -> Dict:
        """
        Get comparison of all trained models
        
        Returns:
            Dictionary with performance metrics for all models
        """
        comparison = {}
        
        for model_name, metrics in self.model_performance.items():
            comparison[model_name] = {
                'accuracy': f"{metrics['accuracy']:.2f}%",
                'rmse': f"{metrics['rmse']:.4f}",
                'mae': f"{metrics['mae']:.4f}",
                'mape': f"{metrics['mape']:.2f}%",
                'r2': f"{metrics['r2']:.4f}"
            }
        
        return comparison
