import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="BillMitra - Retail Intelligence",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 BillMitra - Retail Intelligence Platform")
st.markdown("**AI-Powered Demand Forecasting & Dynamic Pricing**")

# Sidebar
st.sidebar.header("⚙️ Configuration")

# API URL
API_URL = st.sidebar.text_input("API URL", "http://127.0.0.1:8000")

# Product list
PRODUCTS = [
    "Milk_1L", "Curd_500g", "Paneer_200g", "Rice_5kg", "Wheat_Atta_10kg",
    "Maggi_Pack", "Parle_G_Biscuit", "Lays_Chips", "Kurkure",
    "Tata_Tea_250g", "Nescafe_Coffee", "Coca_Cola_1L",
    "Amul_Ice_Cream", "Dettol_Soap", "Colgate_Toothpaste"
]

selected_product = st.sidebar.selectbox("Select Product", PRODUCTS)
forecast_days = st.sidebar.slider("Forecast Days", 1, 30, 7)

# Tabs
tab1, tab2 = st.tabs(["📈 Demand Forecast", "💰 Dynamic Pricing"])

# TAB 1: DEMAND FORECAST
with tab1:
    if st.button("🔮 Generate Forecast", type="primary", key="forecast_btn"):
        with st.spinner("Generating forecast..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict",
                    json={"product": selected_product, "days_ahead": forecast_days}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state['forecast_data'] = data
                    st.success("✅ Forecast generated successfully!")
                else:
                    st.error(f"❌ Error: {response.json()['detail']}")
            except Exception as e:
                st.error(f"❌ Failed to connect to API: {str(e)}")
    
    if 'forecast_data' in st.session_state:
        data = st.session_state['forecast_data']
        df_forecast = pd.DataFrame({
            'Date': data['forecast_dates'],
            'Predicted Sales': data['forecast_values']
        })
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Product", data['product'])
        with col2:
            st.metric("Avg Daily Sales", f"{df_forecast['Predicted Sales'].mean():.1f} units")
        with col3:
            st.metric("Total Forecast", f"{df_forecast['Predicted Sales'].sum():.0f} units")
        with col4:
            st.metric("Model Used", data['model_used'])
        
        st.markdown("---")
        st.subheader("📈 Sales Forecast")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_forecast['Date'], y=df_forecast['Predicted Sales'],
            mode='lines+markers', name='Forecast',
            line=dict(color='#1f77b4', width=3), marker=dict(size=8)
        ))
        fig.update_layout(
            title=f"{data['product']} - {forecast_days} Day Forecast",
            xaxis_title="Date", yaxis_title="Predicted Sales (units)",
            hovermode='x unified', height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📋 Forecast Data")
        st.dataframe(df_forecast, use_container_width=True)
        
        csv = df_forecast.to_csv(index=False)
        st.download_button(
            "⬇️ Download Forecast CSV", csv,
            file_name=f"{data['product']}_forecast.csv", mime="text/csv"
        )
    else:
        st.info("👈 Click 'Generate Forecast' to get started!")

# TAB 2: DYNAMIC PRICING
with tab2:
    st.markdown("### 💰 AI-Powered Dynamic Pricing Engine")
    
    col1, col2 = st.columns(2)
    with col1:
        price_elasticity = st.slider(
            "Price Elasticity (%)", 
            min_value=5, max_value=20, value=10, step=1,
            help="Maximum price change allowed (10% = ±10% price adjustment)"
        ) / 100
    
    if st.button("💵 Generate Pricing Strategy", type="primary", key="pricing_btn"):
        with st.spinner("Calculating optimal pricing..."):
            try:
                response = requests.post(
                    f"{API_URL}/pricing",
                    json={
                        "product": selected_product,
                        "days_ahead": forecast_days,
                        "price_elasticity": price_elasticity
                    }
                )
                
                if response.status_code == 200:
                    pricing_data = response.json()
                    st.session_state['pricing_data'] = pricing_data
                    st.success("✅ Pricing strategy generated!")
                else:
                    st.error(f"❌ Error: {response.json()['detail']}")
            except Exception as e:
                st.error(f"❌ Failed to connect to API: {str(e)}")
    
    if 'pricing_data' in st.session_state:
        pricing = st.session_state['pricing_data']
        strategy = pricing['overall_strategy']
        daily = pricing['daily_recommendations']
        
        # Overall metrics
        st.subheader("📊 Overall Strategy")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Base Price",
                f"₹{strategy['base_price']:.2f}"
            )
        with col2:
            st.metric(
                "Avg Recommended Price",
                f"₹{strategy['recommended_avg_price']:.2f}",
                delta=f"{strategy['recommended_avg_price'] - strategy['base_price']:.2f}"
            )
        with col3:
            st.metric(
                "Revenue Increase",
                f"{strategy['potential_revenue_increase']:.1f}%",
                delta=f"{strategy['potential_revenue_increase']:.1f}%"
            )
        with col4:
            st.metric(
                "Peak Demand",
                f"{strategy['peak_demand']:.0f} units"
            )
        
        st.markdown("---")
        
        # Daily pricing chart
        st.subheader("📈 Daily Pricing Recommendations")
        
        df_pricing = pd.DataFrame(daily)
        
        fig = go.Figure()
        
        # Base price line
        fig.add_trace(go.Scatter(
            x=df_pricing['day'],
            y=[strategy['base_price']] * len(df_pricing),
            mode='lines',
            name='Base Price',
            line=dict(color='gray', dash='dash', width=2)
        ))
        
        # Recommended price
        fig.add_trace(go.Scatter(
            x=df_pricing['day'],
            y=df_pricing['recommended_price'],
            mode='lines+markers',
            name='Recommended Price',
            line=dict(color='green', width=3),
            marker=dict(size=8)
        ))
        
        # Demand (secondary axis)
        fig.add_trace(go.Bar(
            x=df_pricing['day'],
            y=df_pricing['forecasted_demand'],
            name='Forecasted Demand',
            yaxis='y2',
            opacity=0.3,
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title=f"{pricing['product']} - Dynamic Pricing Strategy",
            xaxis_title="Day",
            yaxis_title="Price (₹)",
            yaxis2=dict(title="Demand (units)", overlaying='y', side='right'),
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Pricing table
        st.subheader("📋 Detailed Pricing Schedule")
        
        df_pricing_display = df_pricing[['day', 'forecasted_demand', 'base_price', 
                                          'recommended_price', 'price_change', 'adjustment', 'reason']]
        df_pricing_display.columns = ['Day', 'Demand', 'Base Price (₹)', 
                                       'Recommended (₹)', 'Change (%)', 'Action', 'Reason']
        
        st.dataframe(df_pricing_display, use_container_width=True)
        
        # Download
        csv_pricing = df_pricing_display.to_csv(index=False)
        st.download_button(
            "⬇️ Download Pricing Strategy CSV",
            csv_pricing,
            file_name=f"{pricing['product']}_pricing_strategy.csv",
            mime="text/csv"
        )
    else:
        st.info("👆 Click 'Generate Pricing Strategy' to see AI-powered recommendations!")
        
        st.markdown("""
        ### 🎯 How Dynamic Pricing Works:
        
        **High Demand Days** (>20% above average):
        - ↗️ Increase price to maximize revenue
        - Capture willingness to pay premium
        
        **Normal Demand Days**:
        - ➡️ Maintain base price
        - Standard profitability
        
        **Low Demand Days** (<20% below average):
        - ↘️ Decrease price to stimulate sales
        - Clear inventory, attract customers
        
        **Result:** Optimize revenue across demand cycles!
        """)

# Footer
st.markdown("---")
st.markdown("**BillMitra** | Built with ❤️ using FastAPI, Prophet ML, and Streamlit")