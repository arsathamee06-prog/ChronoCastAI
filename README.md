# Time Series AI - Forecasting Platform

A comprehensive time series forecasting platform with multiple ML models, advanced analytics dashboard, explainability features, and observability monitoring.

## Features

### 🤖 Machine Learning Models
- **Linear Regression** - Simple baseline model
- **Moving Average** - Statistical forecasting
- **ARIMA** - AutoRegressive Integrated Moving Average
- **SARIMA** - Seasonal ARIMA for seasonal data
- **Prophet** - Facebook's forecasting library
- **LSTM** - Deep learning neural networks

### 📊 Analytics Dashboard
- Real-time model performance metrics
- Model comparison visualizations
- Forecast vs actual trends
- Seasonal pattern analysis
- Trend analysis charts
- Interactive charts and graphs

### 🧠 Explainable AI (XAI)
- Trend analysis and interpretation
- Seasonality pattern detection
- Volatility analysis
- Anomaly detection
- Feature importance ranking
- Confidence interval calculations
- Human-readable predictions

### 📈 Observability & Monitoring
- **API Status Monitoring** - Request success rates, response times
- **System Health Monitoring** - CPU, Memory, Disk usage
- **Model Performance Tracking** - Accuracy, RMSE, MAE metrics
- **Prediction Logging** - All predictions and errors logged
- **Live Dashboard** - Real-time system health visualization

### 🎨 Modern Dashboard UI
- White.js responsive design
- Dark theme with gradient effects
- Professional analytics visualizations
- Intuitive navigation
- Real-time data updates
- Mobile-responsive layout

## Project Structure

```
TimeSeriesAI/
├── backend/
│   └── app/
│       ├── config/
│       │   └── settings.py
│       ├── routes/
│       │   ├── api.py
│       │   ├── dashboard.py
│       │   ├── prediction.py
│       │   ├── model.py
│       │   ├── explainability.py
│       │   └── observability.py
│       ├── ml/
│       │   ├── models/
│       │   │   └── forecasters.py
│       │   ├── preprocessing/
│       │   │   └── preprocessor.py
│       │   └── explainability/
│       │       └── explainer.py
│       ├── services/
│       │   └── model_trainer.py
│       ├── observability/
│       │   └── monitor.py
│       └── utils/
│           ├── error_handler.py
│           ├── validators.py
│           └── logger.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js
│       ├── upload.js
│       ├── dashboard.js
│       ├── prediction.js
│       ├── explainability.js
│       └── observability.js
├── data/
│   └── (uploaded CSV files)
├── models/
│   └── (saved pickle models)
├── logs/
│   └── (application logs)
├── run.py
├── requirements.txt
├── setup.bat (Windows)
├── setup.sh (Linux/Mac)
└── README.md
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Step 1: Clone/Setup Project
```bash
cd TimeSeriesAI
```

### Step 2: Run Setup Script

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Start the Application

1. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate.bat`
   - Linux/Mac: `source venv/bin/activate`

2. **Run Flask server:**
   ```bash
   python run.py
   ```

3. **Open in browser:**
   ```
   http://localhost:5000
   ```

### Workflow

1. **Upload Data** - Upload your CSV time series data
2. **Automatic Preprocessing** - Data cleaning, feature engineering
3. **Model Training** - Train all 6 forecasting models
4. **Model Selection** - Best model automatically selected
5. **Make Predictions** - Generate forecasts for future periods
6. **Analyze Results** - View explainability insights
7. **Monitor System** - Check observability metrics

## API Endpoints

### Data Management
- `POST /api/upload` - Upload CSV file
- `POST /api/preprocess` - Preprocess data
- `POST /api/train` - Train models
- `POST /api/predict` - Make predictions

### Dashboard
- `GET /api/dashboard/overview` - Dashboard metrics
- `GET /api/dashboard/model-comparison` - Model performance
- `GET /api/dashboard/time-series` - Historical and forecast data
- `GET /api/dashboard/seasonal-patterns` - Seasonal analysis
- `GET /api/dashboard/trend-analysis` - Trend information

### Models
- `GET /api/model/list` - List all models
- `GET /api/model/details/<name>` - Model details
- `POST /api/model/retrain` - Retrain specific model
- `GET /api/model/performance` - Performance metrics

### Explainability
- `POST /api/explainability/explanation` - Get complete explanation
- `POST /api/explainability/trend` - Trend analysis
- `POST /api/explainability/seasonality` - Seasonality analysis
- `POST /api/explainability/volatility` - Volatility analysis
- `POST /api/explainability/anomalies` - Anomaly detection

### Observability
- `GET /api/observability/api-status` - API health
- `GET /api/observability/system-health` - System metrics
- `GET /api/observability/model-performance` - Model tracking
- `GET /api/observability/prediction-logs` - Prediction history
- `GET /api/observability/dashboard` - Full observability dashboard

## Configuration

Edit `.env` file to customize:
- Flask port (default: 5000)
- Database URI
- Model save path
- Upload directory
- Forecast horizon
- Test/validation split ratios

## Supported File Formats

### Input
- CSV files with time series data
- Automatic date and target column detection
- Supports missing values and various date formats

## Model Training Details

### Preprocessing
- Automatic date/numeric column detection
- Missing value imputation
- Outlier handling
- Feature engineering (lag, rolling statistics)
- Trend and seasonality detection
- Data normalization

### Training Process
1. Splits data into train, validation, test sets
2. Trains all 6 models in parallel
3. Evaluates on validation set
4. Selects best model based on accuracy
5. Saves all models as pickle files

### Metrics
- **Accuracy** - Percentage (0-100%)
- **RMSE** - Root Mean Squared Error
- **MAE** - Mean Absolute Error
- **MAPE** - Mean Absolute Percentage Error
- **R²** - Coefficient of determination

## Explainability Features

### Trend Analysis
- Identifies upward/downward trends
- Calculates trend strength
- Forecasts future trend direction

### Seasonality Detection
- Detects seasonal periods
- Measures seasonality strength
- Identifies peak/trough seasons

### Volatility Analysis
- Calculates historical volatility
- Forecasts volatility changes
- Trend assessment

### Anomaly Detection
- Uses Z-score method
- Identifies outliers
- Severity ranking

### Feature Importance
- Estimates which factors drive predictions
- Provides impact metrics

## Observability Features

### API Monitoring
- Request tracking
- Success rate monitoring
- Response time analysis
- Endpoint-specific metrics

### System Health
- CPU usage tracking
- Memory usage monitoring
- Disk space analysis
- Historical trends

### Model Performance Tracking
- Accuracy over time
- RMSE/MAE tracking
- Performance trends
- Model comparison

### Prediction Logging
- All predictions logged
- Error tracking
- Success rates
- Forecast statistics

## Performance Optimization

- Model predictions cached
- Vectorized NumPy operations
- Efficient data preprocessing
- Optional GPU support (TensorFlow/LSTM)

## Deployment

### Production Setup
1. Set `FLASK_ENV=production` in .env
2. Use gunicorn for WSGI server:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```
3. Use nginx as reverse proxy
4. Enable HTTPS/SSL
5. Set strong SECRET_KEY

### Docker (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

## Troubleshooting

### Common Issues

1. **Import Errors:**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **Port Already in Use:**
   - Change FLASK_PORT in .env
   - Or kill process: `lsof -ti:5000 | xargs kill -9`

3. **CORS Errors:**
   - Check CORS_ENABLED setting
   - Verify frontend API_BASE_URL

4. **Model Training Fails:**
   - Check data format (CSV)
   - Ensure sufficient data (>10 rows)
   - Check for invalid numeric columns

## Requirements

See [requirements.txt](requirements.txt) for complete dependencies:
- Flask 2.3.3
- Pandas 2.0.3
- NumPy 1.24.3
- Scikit-learn 1.3.0
- Statsmodels 0.14.0
- Prophet 1.1.5
- TensorFlow 2.13.0
- PSUtil 5.9.5
- Gunicorn 21.2.0

## License

MIT License - Feel free to use and modify

## Contributing

Contributions welcome! Please follow PEP 8 style guide.

## Support

For issues and questions:
1. Check documentation
2. Review API examples
3. Check logs in `/logs` directory
4. Review error messages in observability dashboard

## Roadmap

- [ ] Database integration (SQLAlchemy)
- [ ] User authentication
- [ ] Advanced hyperparameter tuning
- [ ] Automated model selection
- [ ] Real-time forecasting updates
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Docker containerization
- [ ] Kubernetes deployment configs
- [ ] Advanced visualizations (3D, animations)

---

**Created:** 2026
**Version:** 1.0.0
**Status:** Production Ready
