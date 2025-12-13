from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import joblib
import pandas as pd
from datetime import datetime, timedelta
import os

# Initialize FastAPI app
app = FastAPI(
    title="BillMitra Forecasting API",
    description="Demand forecasting API for retail products",
    version="1.0.0"
)

# Load models and data
# Use forward slashes (easier!)
MODELS_PATH = "C:/Users/karta/Documents/billmitra/models"
DATA_PATH = "C:/Users/karta/Documents/billmitra/data/processed/featured_indian_retail.csv"
# Load data
df = pd.read_csv(DATA_PATH)
df['Date'] = pd.to_datetime(df['Date'])

# Request/Response models
class PredictionRequest(BaseModel):
    product: str
    days_ahead: int = 7

class PredictionResponse(BaseModel):
    product: str
    forecast_dates: List[str]
    forecast_values: List[float]
    model_used: str

# Routes
@app.get("/")
def read_root():
    return {
        "message": "Welcome to BillMitra Forecasting API",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Get forecast",
            "/products": "GET - List products",
            "/docs": "GET - API documentation"
        }
    }

@app.get("/products")
def get_products():
    """List all available products"""
    products = df['ProductName'].unique().tolist()
    return {
        "count": len(products),
        "products": products
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """
    Generate forecast for a product
    """
    product = request.product
    days = request.days_ahead
    
    # Validate product
    if product not in df['ProductName'].values:
        raise HTTPException(status_code=404, detail=f"Product '{product}' not found")
    
    # Load model
    model_path = f"{MODELS_PATH}/prophet_{product}.pkl"
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail=f"Model for '{product}' not found")
    
    model = joblib.load(model_path)
    
    # Generate future dates
    last_date = df[df['ProductName'] == product]['Date'].max()
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=days, freq='D')
    
    # Create future dataframe
    future_df = pd.DataFrame({'ds': future_dates})
    
    # Predict
    forecast = model.predict(future_df)
    
    return {
        "product": product,
        "forecast_dates": forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
        "forecast_values": forecast['yhat'].round(2).tolist(),
        "model_used": "Prophet"
    }

@app.get("/historical/{product}")
def get_historical(product: str, days: int = 30):
    """Get historical sales data"""
    if product not in df['ProductName'].values:
        raise HTTPException(status_code=404, detail=f"Product '{product}' not found")
    
    product_df = df[df['ProductName'] == product].tail(days)
    
    return {
        "product": product,
        "period": f"Last {days} days",
        "data": product_df[['Date', 'QuantitySold']].to_dict('records')
    }

# Run with: uvicorn main:app --reload