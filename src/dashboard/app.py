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

# Product list (hardcoded for now)
PRODUCTS = [
    "Milk_1L",
    "Curd_500g",
    "Paneer_200g",
    "Rice_5kg",
    "Wheat_Atta_10kg",
    "Maggi_Pack",
    "Parle_G_Biscuit",
    "Lays_Chips",
    "Kurkure",
    "Tata_Tea_250g",
    "Nescafe_Coffee",
    "Coca_Cola_1L",
    "Amul_Ice_Cream",
    "Dettol_Soap",
    "Colgate_Toothpaste"
]

# Select product
selected_product = st.sidebar.selectbox("Select Product", PRODUCTS)

# Forecast days
forecast_days = st.sidebar.slider("Forecast Days", 1, 30, 7)

# Predict button
if st.sidebar.button("🔮 Generate Forecast", type="primary"):
    
    with st.spinner("Generating forecast..."):
        try:
            # Call API
            response = requests.post(
                f"{API_URL}/predict",
                json={
                    "product": selected_product,
                    "days_ahead": forecast_days
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Store in session state
                st.session_state['forecast_data'] = data
                st.success("✅ Forecast generated successfully!")
            else:
                st.error(f"❌ Error: {response.json()['detail']}")
                
        except Exception as e:
            st.error(f"❌ Failed to connect to API: {str(e)}")

# Display forecast if available
if 'forecast_data' in st.session_state:
    data = st.session_state['forecast_data']
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': data['forecast_dates'],
        'Predicted Sales': data['forecast_values']
    })
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Product",
            data['product'],
            delta=None
        )
    
    with col2:
        st.metric(
            "Avg Daily Sales",
            f"{df['Predicted Sales'].mean():.1f} units"
        )
    
    with col3:
        st.metric(
            "Total Forecast",
            f"{df['Predicted Sales'].sum():.0f} units"
        )
    
    with col4:
        st.metric(
            "Model Used",
            data['model_used']
        )
    
    st.markdown("---")
    
    # Chart
    st.subheader("📈 Sales Forecast")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Predicted Sales'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=f"{data['product']} - {forecast_days} Day Forecast",
        xaxis_title="Date",
        yaxis_title="Predicted Sales (units)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("📋 Forecast Data")
    st.dataframe(df, use_container_width=True)
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Forecast CSV",
        data=csv,
        file_name=f"{data['product']}_forecast.csv",
        mime="text/csv"
    )

else:
    st.info("👈 Select a product and click 'Generate Forecast' to get started!")
    
    # Show sample image or instructions
    st.markdown("""
    ### 🚀 How to Use:
    
    1. **Select a product** from the sidebar
    2. **Choose forecast period** (1-30 days)
    3. **Click 'Generate Forecast'**
    4. **View predictions** with interactive charts
    5. **Download results** as CSV
    
    ### 📊 Features:
    - Real-time demand forecasting
    - Interactive visualizations
    - Multiple product categories
    - Export capabilities
    """)

# Footer
st.markdown("---")
st.markdown("**BillMitra** | Built with ❤️ using FastAPI, Prophet ML, and Streamlit")