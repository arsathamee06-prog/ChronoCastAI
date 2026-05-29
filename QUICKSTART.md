# Quick Start Guide - Time Series AI Forecasting Platform

## 🚀 Get Started in 5 Minutes

### Step 1: Setup (1 minute)
**Windows:**
```bash
cd TimeSeriesAI
setup.bat
```

**Linux/Mac:**
```bash
cd TimeSeriesAI
chmod +x setup.sh
./setup.sh
```

### Step 2: Activate Virtual Environment (30 seconds)
**Windows:**
```bash
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 3: Generate Sample Data (30 seconds)
```bash
python generate_sample_data.py 365
```
This creates `sample_timeseries.csv` with 365 days of sample data.

### Step 4: Start the Application (30 seconds)
```bash
python run.py
```

### Step 5: Open in Browser (30 seconds)
```
http://localhost:5000
```

## 📋 Workflow

1. **Dashboard Page** - See system health and metrics
2. **Upload Data** - Click "Upload Data" tab
3. **Select File** - Drag & drop or click to select your CSV file
4. **Auto Preprocessing** - System automatically:
   - Detects date and target columns
   - Cleans data
   - Creates features
   - Detects seasonality
5. **Train Models** - Click "Train Models" button
   - Trains all 6 models (Linear Regression, Moving Average, ARIMA, SARIMA, Prophet, LSTM)
   - Automatically selects best model
   - Saves trained model
6. **Make Predictions** - Go to "Predict" tab
   - Set forecast horizon (days)
   - Generate forecast
7. **View Explanations** - Go to "Explain" tab
   - Understand trends
   - See seasonal patterns
   - Check volatility
   - Detect anomalies
8. **Monitor System** - Go to "Monitor" tab
   - Check API health
   - View system resources
   - See model performance

## 📁 Project Structure

```
TimeSeriesAI/
├── backend/          # Python Flask backend
├── frontend/         # HTML/CSS/JS dashboard
├── data/            # Uploaded CSV files
├── models/          # Saved pickle models
├── logs/            # Application logs
├── run.py           # Main entry point
└── requirements.txt # Dependencies
```

## 🎯 Key Features

✅ **6 Forecasting Models**
- Linear Regression
- Moving Average
- ARIMA
- SARIMA
- Prophet
- LSTM Neural Networks

✅ **Automatic Preprocessing**
- Date/column detection
- Missing value handling
- Feature engineering
- Seasonality detection

✅ **Advanced Dashboard**
- Model comparison charts
- Forecast visualization
- Seasonal patterns
- Trend analysis

✅ **Explainability (XAI)**
- Why predictions increase/decrease
- Trend analysis
- Seasonality insights
- Volatility assessment
- Anomaly detection
- Confidence intervals

✅ **Observability Monitoring**
- API health status
- System resources (CPU, Memory, Disk)
- Prediction logs
- Model performance tracking

## 📊 CSV File Format

Your CSV should have:
- Date column (any common format: YYYY-MM-DD, MM/DD/YYYY, etc.)
- Numeric column(s) with values to forecast
- Column headers

**Example:**
```csv
date,value,volume
2023-01-01,100.5,500
2023-01-02,101.2,510
2023-01-03,100.8,495
...
```

## 🔧 Configuration

Edit `.env` for:
- API port (default: 5000)
- Forecast horizon
- Model save location
- Log level

## 📈 Expected Results

After training, you'll see:
- Best model accuracy (typically 85-95%)
- Model comparison metrics
- Forecast values for next period
- Confidence intervals
- Trend direction (up/down)
- Seasonal pattern information

## ❓ Troubleshooting

**Port 5000 already in use?**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

**Module not found?**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

**API not responding?**
- Check Flask server is running
- Check browser console for errors
- Check logs in `/logs` folder

## 📚 API Examples

### Upload Data
```bash
curl -X POST http://localhost:5000/api/upload -F "file=@sample.csv"
```

### Get Predictions
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"model_path": "models/best_model.pkl", "forecast_horizon": 30}'
```

### Get Explainability
```bash
curl -X POST http://localhost:5000/api/explainability/explanation \
  -H "Content-Type: application/json" \
  -d '{"historical_data": [...], "forecast_data": [...], "seasonal_period": 12}'
```

## 🌐 Dashboard Pages

1. **Dashboard** - System overview and metrics
2. **Upload Data** - Data upload and preprocessing
3. **Models** - Model comparison and details
4. **Predict** - Generate forecasts
5. **Explain** - XAI insights
6. **Monitor** - System health monitoring

## 🎓 Learning Resources

- Check README.md for detailed documentation
- Review API endpoints in routes/
- Check ML models in ml/models/
- Explore sample output from generate_sample_data.py

## 🚀 Next Steps

1. Prepare your time series data (CSV format)
2. Run setup and start application
3. Upload your data
4. Let AI train best model
5. Generate forecasts
6. Understand predictions with XAI
7. Monitor system health

## 📝 Sample Commands

```bash
# Generate 90 days of sample data
python generate_sample_data.py 90

# With venv activated, start server
python run.py

# Check if running
curl http://localhost:5000/api/health
```

---

**Happy Forecasting! 🎯📈**

For detailed documentation, see [README.md](README.md)
