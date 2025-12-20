from typing import List, Dict
import statistics

def calculate_dynamic_price(
    forecast_values: List[float],
    base_price: float,
    price_elasticity: float = 0.1
) -> Dict:
    """
    Calculate dynamic pricing based on demand forecast
    
    Args:
        forecast_values: List of forecasted sales
        base_price: Current/base price of product
        price_elasticity: How much to adjust price (0.1 = 10% max change)
    
    Returns:
        Dictionary with pricing recommendations
    """
    
    # Calculate statistics
    avg_forecast = statistics.mean(forecast_values)
    max_forecast = max(forecast_values)
    min_forecast = min(forecast_values)
    
    # Pricing strategy
    pricing_recommendations = []
    
    for i, forecast in enumerate(forecast_values):
        # Calculate demand ratio (compared to average)
        demand_ratio = forecast / avg_forecast if avg_forecast > 0 else 1.0
        
        # Price adjustment based on demand
        if demand_ratio > 1.2:  # High demand (20% above average)
            adjustment = "INCREASE"
            new_price = base_price * (1 + price_elasticity)
            reason = "High demand expected - increase price to maximize revenue"
            
        elif demand_ratio < 0.8:  # Low demand (20% below average)
            adjustment = "DECREASE"
            new_price = base_price * (1 - price_elasticity)
            reason = "Low demand expected - decrease price to stimulate sales"
            
        else:  # Normal demand
            adjustment = "MAINTAIN"
            new_price = base_price
            reason = "Normal demand - maintain current price"
        
        pricing_recommendations.append({
            "day": i + 1,
            "forecasted_demand": round(forecast, 2),
            "base_price": round(base_price, 2),
            "recommended_price": round(new_price, 2),
            "price_change": round(((new_price - base_price) / base_price) * 100, 1),
            "adjustment": adjustment,
            "reason": reason
        })
    
    # Overall strategy
    overall_strategy = {
        "average_demand": round(avg_forecast, 2),
        "peak_demand": round(max_forecast, 2),
        "low_demand": round(min_forecast, 2),
        "base_price": round(base_price, 2),
        "recommended_avg_price": round(statistics.mean([p["recommended_price"] for p in pricing_recommendations]), 2),
        "potential_revenue_increase": round(
            sum([p["recommended_price"] * forecast_values[i] for i, p in enumerate(pricing_recommendations)]) / 
            sum([base_price * f for f in forecast_values]) * 100 - 100, 
            1
        )
    }
    
    return {
        "daily_recommendations": pricing_recommendations,
        "overall_strategy": overall_strategy
    }


# Product base prices (hardcoded for demo - in production would come from database)
PRODUCT_BASE_PRICES = {
    "Milk_1L": 60.0,
    "Curd_500g": 40.0,
    "Paneer_200g": 90.0,
    "Rice_5kg": 250.0,
    "Wheat_Atta_10kg": 450.0,
    "Maggi_Pack": 12.0,
    "Parle_G_Biscuit": 10.0,
    "Lays_Chips": 20.0,
    "Kurkure": 20.0,
    "Tata_Tea_250g": 120.0,
    "Nescafe_Coffee": 150.0,
    "Coca_Cola_1L": 40.0,
    "Amul_Ice_Cream": 80.0,
    "Dettol_Soap": 35.0,
    "Colgate_Toothpaste": 45.0
}