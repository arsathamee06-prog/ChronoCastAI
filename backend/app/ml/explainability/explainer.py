"""
Explainability and Interpretability Module
Provides insights into forecasting predictions
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from scipy import stats

class TimeSeriesExplainer:
    """Explains time series forecasting predictions"""
    
    def __init__(self, historical_data: np.ndarray, forecast: np.ndarray, 
                 dates: pd.DatetimeIndex = None):
        """
        Initialize explainer
        
        Args:
            historical_data: Historical time series data
            forecast: Forecasted values
            dates: DatetimeIndex for the historical data
        """
        self.historical_data = historical_data
        self.forecast = forecast
        self.dates = dates
        self.last_value = historical_data[-1]
    
    def trend_analysis(self) -> Dict:
        """
        Analyze trend in the data
        
        Returns:
            Dictionary with trend analysis
        """
        # Calculate trend using linear regression
        x = np.arange(len(self.historical_data))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, self.historical_data)
        
        # Forecast trend
        forecast_slope, forecast_intercept, forecast_r, _, _ = stats.linregress(
            np.arange(len(self.historical_data) - len(self.historical_data) // 4, len(self.historical_data)),
            self.historical_data[-len(self.historical_data) // 4:]
        )
        
        # Calculate trend percentage
        trend_strength = abs(slope) / (np.std(self.historical_data) + 1e-10) * 100
        
        return {
            'overall_trend': 'upward' if slope > 0 else 'downward',
            'trend_strength': float(trend_strength),
            'slope': float(slope),
            'r_squared': float(r_value ** 2),
            'recent_trend': 'upward' if forecast_slope > 0 else 'downward',
            'recent_slope': float(forecast_slope),
            'forecast_direction': 'increasing' if np.mean(self.forecast) > self.last_value else 'decreasing',
            'forecast_change_percentage': float(((np.mean(self.forecast) - self.last_value) / abs(self.last_value) * 100) if self.last_value != 0 else 0)
        }
    
    def seasonality_analysis(self, period: int = 12) -> Dict:
        """
        Analyze seasonal patterns
        
        Args:
            period: Seasonal period (default: 12 for monthly data)
        
        Returns:
            Dictionary with seasonality analysis
        """
        if len(self.historical_data) < period * 2:
            return {'has_seasonality': False, 'period': period}
        
        # Calculate seasonal component
        seasonal_values = []
        for i in range(period):
            seasonal_values.append(np.mean(self.historical_data[i::period]))
        
        # Check variance of seasonal components
        seasonal_variance = np.var(seasonal_values)
        overall_variance = np.var(self.historical_data)
        seasonality_strength = seasonal_variance / (overall_variance + 1e-10) * 100
        
        # Find peak and trough seasons
        peak_season = np.argmax(seasonal_values) + 1
        trough_season = np.argmin(seasonal_values) + 1
        
        return {
            'has_seasonality': seasonality_strength > 10,
            'seasonality_strength': float(seasonality_strength),
            'period': period,
            'peak_season': int(peak_season),
            'trough_season': int(trough_season),
            'seasonal_amplitude': float(np.max(seasonal_values) - np.min(seasonal_values)),
            'peak_value': float(np.max(seasonal_values)),
            'trough_value': float(np.min(seasonal_values))
        }
    
    def volatility_analysis(self, window: int = 30) -> Dict:
        """
        Analyze volatility in the data
        
        Args:
            window: Rolling window size
        
        Returns:
            Dictionary with volatility analysis
        """
        # Calculate volatility (rolling standard deviation)
        returns = np.diff(self.historical_data) / self.historical_data[:-1]
        volatility = np.std(returns) * 100
        
        # Recent volatility
        recent_volatility = np.std(returns[-window:]) * 100 if len(returns) >= window else volatility
        
        # Forecast volatility
        forecast_diff = np.diff(self.forecast) / self.forecast[:-1]
        forecast_volatility = np.std(forecast_diff) * 100 if len(self.forecast) > 1 else 0
        
        return {
            'overall_volatility': float(volatility),
            'recent_volatility': float(recent_volatility),
            'forecast_volatility': float(forecast_volatility),
            'volatility_trend': 'increasing' if forecast_volatility > recent_volatility else 'decreasing',
            'volatility_level': 'high' if volatility > np.percentile([volatility, recent_volatility, forecast_volatility], 75) else 'low'
        }
    
    def anomaly_detection(self) -> Dict:
        """
        Detect anomalies in the historical data
        
        Returns:
            Dictionary with anomaly information
        """
        # Use z-score method
        z_scores = np.abs(stats.zscore(self.historical_data))
        threshold = 3
        anomalies = np.where(z_scores > threshold)[0]
        
        anomaly_info = {
            'anomaly_count': int(len(anomalies)),
            'anomaly_percentage': float(len(anomalies) / len(self.historical_data) * 100),
            'anomaly_indices': anomalies.tolist()[:10],  # Top 10 anomalies
            'anomaly_severity': float(np.max(z_scores)) if len(z_scores) > 0 else 0
        }
        
        return anomaly_info
    
    def feature_importance(self) -> Dict:
        """
        Estimate feature importance for forecasting
        
        Returns:
            Dictionary with feature importance estimates
        """
        # Analyze recent values vs historical average
        recent_window = len(self.historical_data) // 4
        recent_avg = np.mean(self.historical_data[-recent_window:])
        historical_avg = np.mean(self.historical_data[:-recent_window])
        
        # Calculate impact factors
        mean_impact = abs(recent_avg - historical_avg) / (abs(historical_avg) + 1e-10) * 100
        
        # Variance impact
        recent_var = np.var(self.historical_data[-recent_window:])
        historical_var = np.var(self.historical_data[:-recent_window])
        var_impact = abs(recent_var - historical_var) / (abs(historical_var) + 1e-10) * 100
        
        return {
            'recent_level_impact': float(mean_impact),
            'volatility_impact': float(var_impact),
            'driving_factors': ['recent_trend', 'volatility', 'seasonality'],
            'forecast_influenced_by': {
                'recent_trend': True,
                'seasonal_patterns': True,
                'volatility': True,
                'anomalies': len(self.anomaly_detection()['anomaly_indices']) > 0
            }
        }
    
    def confidence_interval(self, confidence: float = 0.95) -> Dict:
        """
        Calculate confidence intervals for forecast
        
        Args:
            confidence: Confidence level (default: 0.95 for 95%)
        
        Returns:
            Dictionary with confidence intervals
        """
        # Calculate standard error of recent data
        recent_std = np.std(self.historical_data[-len(self.historical_data)//4:])
        
        # Confidence multiplier
        z_score = stats.norm.ppf((1 + confidence) / 2)
        margin_of_error = z_score * recent_std
        
        upper_bound = self.forecast + margin_of_error
        lower_bound = self.forecast - margin_of_error
        
        return {
            'confidence_level': confidence * 100,
            'upper_bound': upper_bound.tolist(),
            'lower_bound': lower_bound.tolist(),
            'margin_of_error': float(margin_of_error),
            'forecast_std': float(recent_std)
        }
    
    def comprehensive_explanation(self, seasonal_period: int = 12) -> Dict:
        """
        Generate comprehensive explanation of forecast
        
        Args:
            seasonal_period: Seasonal period for analysis
        
        Returns:
            Comprehensive dictionary with all explanations
        """
        trend = self.trend_analysis()
        seasonality = self.seasonality_analysis(seasonal_period)
        volatility = self.volatility_analysis()
        anomalies = self.anomaly_detection()
        features = self.feature_importance()
        confidence = self.confidence_interval()
        
        # Generate explanation text
        explanation = self._generate_explanation_text(trend, seasonality, volatility)
        
        return {
            'summary': explanation,
            'trend_analysis': trend,
            'seasonality_analysis': seasonality,
            'volatility_analysis': volatility,
            'anomaly_detection': anomalies,
            'feature_importance': features,
            'confidence_interval': confidence,
            'forecast_values': self.forecast.tolist()
        }
    
    def _generate_explanation_text(self, trend: Dict, seasonality: Dict, volatility: Dict) -> str:
        """
        Generate human-readable explanation text
        
        Args:
            trend: Trend analysis
            seasonality: Seasonality analysis
            volatility: Volatility analysis
        
        Returns:
            Explanation text
        """
        explanation = []
        
        # Trend explanation
        change_pct = trend['forecast_change_percentage']
        if change_pct > 0:
            explanation.append(f"The forecast shows an {trend['forecast_direction']} trend with values expected to increase by approximately {abs(change_pct):.2f}%.")
        else:
            explanation.append(f"The forecast shows a {trend['forecast_direction']} trend with values expected to decrease by approximately {abs(change_pct):.2f}%.")
        
        explanation.append(f"The overall trend is {trend['overall_trend']} with a strength of {trend['trend_strength']:.2f}.")
        
        # Seasonality explanation
        if seasonality['has_seasonality']:
            explanation.append(f"The data exhibits seasonal patterns with a period of {seasonality['period']} and seasonality strength of {seasonality['seasonality_strength']:.2f}%.")
        
        # Volatility explanation
        if volatility['volatility_level'] == 'high':
            explanation.append(f"The data has high volatility with recent volatility at {volatility['recent_volatility']:.2f}%.")
        else:
            explanation.append(f"The data is relatively stable with low volatility at {volatility['overall_volatility']:.2f}%.")
        
        return " ".join(explanation)
