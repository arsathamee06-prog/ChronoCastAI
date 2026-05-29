"""
Observability and Monitoring Module
Tracks API status, predictions, system health, and model performance
"""
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import psutil
from collections import deque

class PredictionLogger:
    """Log all predictions made by the system"""
    
    def __init__(self, log_file: str = 'logs/predictions.log', max_entries: int = 10000):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.max_entries = max_entries
        self.predictions = deque(maxlen=max_entries)
    
    def log_prediction(self, model_name: str, input_data: Dict, 
                      forecast: List, accuracy: float, confidence: float) -> None:
        """
        Log a prediction
        
        Args:
            model_name: Name of the model used
            input_data: Input data information
            forecast: Forecasted values
            accuracy: Model accuracy
            confidence: Confidence level
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'model_name': model_name,
            'input_shape': input_data.get('shape'),
            'forecast_length': len(forecast) if isinstance(forecast, list) else 0,
            'accuracy': accuracy,
            'confidence': confidence,
            'forecast_mean': sum(forecast) / len(forecast) if forecast else 0,
            'status': 'success'
        }
        
        self.predictions.append(log_entry)
        self._write_to_file(log_entry)
    
    def log_error(self, model_name: str, error_message: str) -> None:
        """
        Log a prediction error
        
        Args:
            model_name: Name of the model
            error_message: Error message
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'model_name': model_name,
            'error': error_message,
            'status': 'error'
        }
        
        self.predictions.append(log_entry)
        self._write_to_file(log_entry)
    
    def _write_to_file(self, entry: Dict) -> None:
        """Write log entry to file"""
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"Error writing to log file: {str(e)}")
    
    def get_recent_predictions(self, limit: int = 100) -> List[Dict]:
        """Get recent predictions"""
        return list(self.predictions)[-limit:]
    
    def get_prediction_statistics(self) -> Dict:
        """Get statistics about predictions"""
        if not self.predictions:
            return {}
        
        successful = [p for p in self.predictions if p.get('status') == 'success']
        errors = [p for p in self.predictions if p.get('status') == 'error']
        
        accuracies = [p.get('accuracy', 0) for p in successful if 'accuracy' in p]
        
        return {
            'total_predictions': len(self.predictions),
            'successful': len(successful),
            'errors': len(errors),
            'success_rate': (len(successful) / len(self.predictions) * 100) if self.predictions else 0,
            'average_accuracy': sum(accuracies) / len(accuracies) if accuracies else 0,
            'avg_forecast_length': sum(p.get('forecast_length', 0) for p in self.predictions) / len(self.predictions) if self.predictions else 0
        }

class SystemHealthMonitor:
    """Monitor system health and resources"""
    
    def __init__(self, max_history: int = 288):  # 24 hours with 5-minute intervals
        self.max_history = max_history
        self.health_history = deque(maxlen=max_history)
    
    def get_system_status(self) -> Dict:
        """Get current system status"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status = {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage_percent': cpu_percent,
            'memory_usage_percent': memory.percent,
            'disk_usage_percent': disk.percent,
            'memory_available_gb': memory.available / (1024 ** 3),
            'api_status': 'healthy' if cpu_percent < 80 and memory.percent < 85 else 'warning',
            'system_status': 'operational' if cpu_percent < 90 and memory.percent < 90 and disk.percent < 90 else 'warning'
        }
        
        self.health_history.append(status)
        return status
    
    def get_health_history(self) -> List[Dict]:
        """Get system health history"""
        return list(self.health_history)
    
    def get_average_health(self) -> Dict:
        """Get average health metrics"""
        if not self.health_history:
            return {}
        
        avg_cpu = sum(h['cpu_usage_percent'] for h in self.health_history) / len(self.health_history)
        avg_memory = sum(h['memory_usage_percent'] for h in self.health_history) / len(self.health_history)
        avg_disk = sum(h['disk_usage_percent'] for h in self.health_history) / len(self.health_history)
        
        return {
            'average_cpu_percent': avg_cpu,
            'average_memory_percent': avg_memory,
            'average_disk_percent': avg_disk,
            'peak_cpu_percent': max(h['cpu_usage_percent'] for h in self.health_history),
            'peak_memory_percent': max(h['memory_usage_percent'] for h in self.health_history)
        }

class ModelPerformanceTracker:
    """Track model performance over time"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.performance_history = deque(maxlen=max_history)
    
    def log_model_performance(self, model_name: str, metrics: Dict) -> None:
        """
        Log model performance metrics
        
        Args:
            model_name: Name of the model
            metrics: Performance metrics dictionary
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'model_name': model_name,
            'accuracy': metrics.get('accuracy', 0),
            'rmse': metrics.get('rmse', 0),
            'mae': metrics.get('mae', 0),
            'mape': metrics.get('mape', 0),
            'r2': metrics.get('r2', 0)
        }
        self.performance_history.append(entry)
    
    def get_model_stats(self, model_name: str = None) -> Dict:
        """Get statistics for a specific model or all models"""
        if not self.performance_history:
            return {}
        
        if model_name:
            entries = [p for p in self.performance_history if p['model_name'] == model_name]
        else:
            entries = list(self.performance_history)
        
        if not entries:
            return {}
        
        accuracies = [e.get('accuracy', 0) for e in entries]
        rmses = [e.get('rmse', 0) for e in entries]
        maes = [e.get('mae', 0) for e in entries]
        
        return {
            'model_name': model_name or 'all_models',
            'total_evaluations': len(entries),
            'average_accuracy': sum(accuracies) / len(accuracies) if accuracies else 0,
            'best_accuracy': max(accuracies) if accuracies else 0,
            'worst_accuracy': min(accuracies) if accuracies else 0,
            'average_rmse': sum(rmses) / len(rmses) if rmses else 0,
            'average_mae': sum(maes) / len(maes) if maes else 0,
            'trend': 'improving' if len(accuracies) > 1 and accuracies[-1] > accuracies[0] else 'stable'
        }
    
    def get_all_model_comparison(self) -> Dict[str, Dict]:
        """Get comparison of all models"""
        models = set(p['model_name'] for p in self.performance_history)
        return {model: self.get_model_stats(model) for model in models}

class APIMonitor:
    """Monitor API calls and performance"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.api_calls = deque(maxlen=max_history)
        self.start_time = time.time()
    
    def log_api_call(self, endpoint: str, method: str, status_code: int, 
                     response_time: float) -> None:
        """
        Log an API call
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            status_code: Response status code
            response_time: Response time in milliseconds
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'method': method,
            'status_code': status_code,
            'response_time_ms': response_time,
            'success': 200 <= status_code < 300
        }
        self.api_calls.append(entry)
    
    def get_api_stats(self, endpoint: str = None) -> Dict:
        """Get API statistics"""
        if not self.api_calls:
            return {}
        
        if endpoint:
            calls = [c for c in self.api_calls if c['endpoint'] == endpoint]
        else:
            calls = list(self.api_calls)
        
        if not calls:
            return {}
        
        response_times = [c['response_time_ms'] for c in calls]
        successful = [c for c in calls if c['success']]
        
        return {
            'endpoint': endpoint or 'all_endpoints',
            'total_calls': len(calls),
            'successful_calls': len(successful),
            'failed_calls': len(calls) - len(successful),
            'success_rate': (len(successful) / len(calls) * 100) if calls else 0,
            'average_response_time_ms': sum(response_times) / len(response_times) if response_times else 0,
            'min_response_time_ms': min(response_times) if response_times else 0,
            'max_response_time_ms': max(response_times) if response_times else 0
        }
    
    def get_uptime(self) -> Dict:
        """Get API uptime information"""
        uptime_seconds = time.time() - self.start_time
        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60
        
        return {
            'uptime_seconds': uptime_seconds,
            'uptime_formatted': f"{int(hours)}h {int(minutes)}m",
            'start_time': datetime.fromtimestamp(self.start_time).isoformat()
        }
    
    def get_health_status(self) -> Dict:
        """Get overall API health status"""
        if not self.api_calls:
            return {'status': 'unknown', 'details': 'No API calls recorded'}
        
        recent_calls = list(self.api_calls)[-100:]  # Last 100 calls
        success_rate = sum(1 for c in recent_calls if c['success']) / len(recent_calls) * 100
        
        avg_response_time = sum(c['response_time_ms'] for c in recent_calls) / len(recent_calls)
        
        if success_rate >= 99 and avg_response_time < 1000:
            status = 'healthy'
        elif success_rate >= 95 and avg_response_time < 2000:
            status = 'good'
        elif success_rate >= 90:
            status = 'degraded'
        else:
            status = 'unhealthy'
        
        return {
            'status': status,
            'success_rate_percent': success_rate,
            'average_response_time_ms': avg_response_time,
            'total_requests': len(list(self.api_calls))
        }
