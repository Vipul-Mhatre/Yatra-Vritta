import streamlit as st
import requests
import os
from PIL import Image

API_URL = "http://127.0.0.1:5000"

st.title("City Feature Explorer")
st.write("This application allows you to explore features of a city based on categories using Overpass API.")

# Step 1: Get Countries
st.header("Step 1: Select Country")
response = requests.get(f"{API_URL}/countries")
if response.status_code == 200:
    countries = response.json()
    selected_country = st.selectbox("Select a Country", countries)
else:
    st.error("Failed to fetch countries.")
    st.stop()

# Step 2: Get Cities
st.header("Step 2: Select City")
if selected_country:
    response = requests.post(f"{API_URL}/cities", json={"country": selected_country})
    if response.status_code == 200:
        cities = response.json()
        selected_city = st.selectbox("Select a City", cities)
    else:
        st.error("Failed to fetch cities.")
        st.stop()

# Step 3: Select Category and Radius
st.header("Step 3: Select Category and Radius")
categories = [
    "medical_tourism",
    "mice",
    "destination_weddings",
]
selected_category = st.selectbox("Select a Category", categories)
radius = st.slider("Select Radius (in meters)", min_value=5000, max_value=100000, value=50000, step=5000)

# Step 4: Process Data
st.header("Step 4: Process Data")
if st.button("Process"):
    with st.spinner("Processing..."):
        payload = {
            "city": selected_city,
            "category": selected_category,
            "radius": radius,
        }
        response = requests.post(f"{API_URL}/process", json=payload)

        if response.status_code == 200:
            result = response.json()
            st.success("Data processed successfully!")

            st.subheader("Download Files")
            st.markdown(f"[Download CSV]({result['csv_file']})", unsafe_allow_html=True)
            st.markdown(f"[Download GeoJSON]({result['geojson_file']})", unsafe_allow_html=True)
            st.markdown(f"[Download Plot]({result['plot_file']})", unsafe_allow_html=True)
            st.markdown(f"[Download Map]({result['map_file']})", unsafe_allow_html=True)

            st.subheader("Plot")
            plot_image_path = result['plot_file']
            if os.path.exists(plot_image_path):
                st.image(Image.open(plot_image_path), caption="Generated Plot")

            st.subheader("Map")
            map_file_path = result['map_file']
            if os.path.exists(map_file_path):
                with open(map_file_path, "r") as map_file:
                    html_content = map_file.read()
                    st.components.v1.html(html_content, height=600)

        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error occurred')}")
