"""
Time Series Data Preprocessing
Handles data loading, cleaning, feature engineering, and preparation
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict, List
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class TimeSeriesPreprocessor:
    """Handles all preprocessing for time series data"""
    
    def __init__(self, df: pd.DataFrame, date_column: str = None, target_column: str = None):
        """
        Initialize preprocessor
        
        Args:
            df: Input DataFrame
            date_column: Column name for dates (auto-detected if None)
            target_column: Column name for target (auto-detected if None)
        """
        self.df = df.copy()
        self.original_df = df.copy()
        self.date_column = date_column
        self.target_column = target_column
        self.scaler = None
        self.scale_params = {}
        self.feature_columns = []
        self.seasonal_period = None
        
    def auto_detect_columns(self) -> Tuple[str, str]:
        """
        Automatically detect date and target columns
        
        Returns:
            Tuple of (date_column, target_column)
        """
        if self.date_column is None:
            # Find date column
            for col in self.df.columns:
                try:
                    pd.to_datetime(self.df[col])
                    self.date_column = col
                    break
                except:
                    pass
        
        if self.target_column is None:
            # Find numeric column with most data
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
            if self.date_column and self.date_column in numeric_cols:
                numeric_cols.remove(self.date_column)
            
            if numeric_cols:
                # Select column with least NaN values
                self.target_column = numeric_cols[0]
                for col in numeric_cols:
                    if self.df[col].notna().sum() > self.df[self.target_column].notna().sum():
                        self.target_column = col
        
        return self.date_column, self.target_column
    
    def clean_data(self) -> pd.DataFrame:
        """Clean data by handling missing values and outliers"""
        # Remove rows with missing target values
        if self.target_column:
            self.df = self.df[self.df[self.target_column].notna()].copy()
        
        # Fill remaining missing values
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            self.df[col].fillna(self.df[col].mean(), inplace=True)
        
        # Remove duplicates
        if self.date_column:
            self.df = self.df.drop_duplicates(subset=[self.date_column], keep='first')
        
        return self.df
    
    def set_datetime_index(self) -> pd.DataFrame:
        """Convert date column to datetime index"""
        if self.date_column:
            self.df[self.date_column] = pd.to_datetime(self.df[self.date_column])
            self.df = self.df.sort_values(self.date_column)
            self.df.set_index(self.date_column, inplace=True)
        
        return self.df
    
    def create_features(self) -> pd.DataFrame:
        """Create time series features"""
        if self.df.index.freq is None:
            self.df = self.df.asfreq(pd.infer_freq(self.df.index) or 'D')
        
        # Trend features
        self.df['trend'] = np.arange(len(self.df))
        
        # Seasonal features
        if isinstance(self.df.index, pd.DatetimeIndex):
            self.df['month'] = self.df.index.month
            self.df['quarter'] = self.df.index.quarter
            self.df['day_of_week'] = self.df.index.dayofweek
            self.df['week'] = self.df.index.isocalendar().week
            self.df['year'] = self.df.index.year
        
        # Lag features
        if self.target_column:
            for lag in [1, 7, 30]:
                if len(self.df) > lag:
                    self.df[f'{self.target_column}_lag_{lag}'] = self.df[self.target_column].shift(lag)
            
            # Rolling statistics
            for window in [7, 30]:
                if len(self.df) > window:
                    self.df[f'{self.target_column}_rolling_mean_{window}'] = self.df[self.target_column].rolling(window).mean()
                    self.df[f'{self.target_column}_rolling_std_{window}'] = self.df[self.target_column].rolling(window).std()
        
        # Remove NaN values created by feature engineering
        self.df = self.df.dropna()
        
        return self.df
    
    def detect_seasonality(self) -> int:
        """Detect seasonal period from data"""
        from scipy import signal
        
        try:
            if self.target_column and len(self.df) > 52:
                # Use autocorrelation to detect seasonality
                ts_values = self.df[self.target_column].values
                
                # Try common seasonal periods
                for period in [7, 12, 30, 365]:
                    if len(ts_values) > period * 2:
                        acf_values = self._calculate_acf(ts_values, nlags=period)
                        if acf_values[period] > 0.3:
                            self.seasonal_period = period
                            return period
            
            self.seasonal_period = 12  # Default
            return 12
        except:
            self.seasonal_period = 12
            return 12
    
    @staticmethod
    def _calculate_acf(x, nlags=40):
        """Calculate autocorrelation function"""
        x = np.asarray(x).squeeze()
        x = x - np.mean(x)
        c0 = np.dot(x, x) / len(x)
        
        acf_values = [1.0]
        for lag in range(1, nlags + 1):
            c_lag = np.dot(x[:-lag], x[lag:]) / len(x)
            acf_values.append(c_lag / c0)
        
        return np.array(acf_values)
    
    def normalize_data(self, method='minmax', columns=None) -> Dict:
        """Normalize data using specified method"""
        if columns is None:
            columns = [self.target_column]
        
        if method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            self.scaler = StandardScaler()
        
        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.scaler.fit_transform(self.df[[col]])
                self.scale_params[col] = {
                    'min': self.df[col].min(),
                    'max': self.df[col].max(),
                    'mean': self.df[col].mean(),
                    'std': self.df[col].std()
                }
        
        return self.scale_params
    
    def split_data(self, test_size=0.2, validation_size=0.1) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Split data into train, validation, and test sets"""
        n = len(self.df)
        train_size = int(n * (1 - test_size - validation_size))
        val_size = int(n * validation_size)
        
        train_df = self.df[:train_size]
        val_df = self.df[train_size:train_size + val_size]
        test_df = self.df[train_size + val_size:]
        
        return train_df, val_df, test_df
    
    def preprocess(self, normalize=True, create_features_flag=True) -> Tuple[pd.DataFrame, Dict]:
        """Complete preprocessing pipeline"""
        self.auto_detect_columns()
        self.clean_data()
        self.set_datetime_index()
        self.detect_seasonality()
        
        if create_features_flag:
            self.create_features()
        
        scale_params = {}
        if normalize:
            scale_params = self.normalize_data(columns=[self.target_column])
        
        return self.df, {
            'date_column': self.date_column,
            'target_column': self.target_column,
            'seasonal_period': self.seasonal_period,
            'scale_params': scale_params,
            'shape': self.df.shape,
            'columns': self.df.columns.tolist()
        }
