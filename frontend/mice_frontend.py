# frontend.py
import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from io import BytesIO

# Configure page
st.set_page_config(page_title="MICE Organize Advisor", page_icon="🏨", layout="wide")

# API configuration
BASE_URL = "http://localhost:5000"

@st.cache_data(ttl=3600)
def get_countries():
    try:
        response = requests.get(f"{BASE_URL}/countries")
        if response.ok:
            return response.json()['countries']
        return []
    except:
        return []

@st.cache_data(ttl=3600)
def get_cities(country):
    try:
        response = requests.get(f"{BASE_URL}/cities", params={'country': country})
        if response.ok:
            return response.json()['cities']
        return []
    except:
        return []

def get_recommendations(country, city):
    try:
        payload = {"country": country, "city": city}
        response = requests.post(f"{BASE_URL}/recommend", json=payload)
        if response.ok:
            return response.json()
        return None
    except:
        return None

# Main app
st.title("🤝 MICE Recommendation System")

# Sidebar
with st.sidebar:
    st.header("Search Parameters")
    countries = get_countries()
    selected_country = st.selectbox("Select Country", options=countries)

    if selected_country:
        cities = get_cities(selected_country)
        selected_city = st.selectbox("Select City", options=cities)

        analyze_btn = st.button("Analyze Destination")

if selected_country and selected_city and analyze_btn:
    with st.spinner("Fetching recommendations..."):
        data = get_recommendations(selected_country, selected_city)

    if data:
        st.header("📊 Key Metrics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("MICE Score", f"{data['selected']['MICE Score']:.1f}")

        with col2:
            st.metric("Tourist Arrivals", f"{data['selected']['Tourist Arrivals']:,}")

        with col3:
            st.metric("International Air Passengers", f"{data['selected']['International Air Passengers']:,}")

        # Visualizations
        st.header("📈 Comparative Analysis")

        tab1, tab2 = st.tabs(["Tourism & Economy", "Safety"])

        with tab1:
            fig = px.scatter(
                pd.DataFrame(data['recommendations']),
                x='GDP per Capita (USD)',
                y='MICE Score',
                size='International Air Passengers',
                hover_data=['name'],
                title='Tourism & Economic Indicators'
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            fig_safety = px.bar(
                pd.DataFrame(data['recommendations']),
                x='name',
                y='Safety Index (Homicide Rate)',
                title="Safety Index Comparison"
            )
            st.plotly_chart(fig_safety, use_container_width=True)

        # Recommendations Section
        st.header("🎯 Top Recommendations")
        recommendations_df = pd.DataFrame(data['recommendations'])[['name', 'countrycode', 'MICE Score', 'Tourist Arrivals', 'International Air Passengers']]
        st.dataframe(recommendations_df)

        # Export Data
        st.header("📤 Export Results")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Export Data (CSV)"):
                csv_data = recommendations_df.to_csv(index=False)
                st.download_button("Download CSV", data=csv_data, file_name="medical_tourism_data.csv", mime="text/csv")

else:
    st.info("👈 Select a country and city from the sidebar to get started.")
