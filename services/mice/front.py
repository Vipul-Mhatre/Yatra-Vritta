import streamlit as st
import requests
import os
from PIL import Image
import streamlit.components.v1 as components
import pandas as pd
import io
import plotly.express as px

API_URL = "http://127.0.0.1:5000"

if "city_data" not in st.session_state:
    st.session_state.city_data = None
if "hotel_data" not in st.session_state:
    st.session_state.hotel_data = None
if "sightseeing_data" not in st.session_state:
    st.session_state.sightseeing_data = None
if "airport_data" not in st.session_state:
    st.session_state.airport_data = None
if "airline_data" not in st.session_state:
    st.session_state.airline_data = None
if "medical_data" not in st.session_state:
    st.session_state.medical_data = None
if "mice_data" not in st.session_state:
    st.session_state.mice_data = None

def display_recommendations(recs, title="Recommendations"):
    st.subheader(title)
    cols = st.columns(2)
    for idx, rec in enumerate(recs):
        col = cols[idx % 2]
        col.markdown(f"**{rec.get('name', 'Unnamed')}**")
        col.write(rec.get('description', ''))
        col.write("---")

def display_analytics(df, chart_title="Analytics"):
    st.subheader("Analytics")
    if not df.empty and "category" in df.columns:
        fig = px.histogram(df, x="category", title=chart_title)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data for analytics.")

def main():
    st.title("City Feature Explorer & More")
    page = st.sidebar.selectbox(
        "Select a Page",
        (
            "City Feature Explorer",
            "Hotel Explorer",
            "Sightseeing Explorer",
            "Airport Explorer",
            "Airline Explorer",
            "Medical Tourism Explorer",
            "MICE Explorer"
        )
    )
    if page == "City Feature Explorer":
        show_city_feature_explorer()
    elif page == "Hotel Explorer":
        show_hotel_explorer()
    elif page == "Sightseeing Explorer":
        show_sightseeing_explorer()
    elif page == "Airport Explorer":
        show_airport_explorer()
    elif page == "Airline Explorer":
        show_airline_explorer()
    elif page == "Medical Tourism Explorer":
        show_medical_explorer()
    elif page == "MICE Explorer":
        show_mice_explorer()

# ---------------------------
# City Feature Explorer
# ---------------------------
def show_city_feature_explorer():
    st.header("City Feature Explorer")
    st.write("Explore features of a city based on different categories using OSM data.")
    st.subheader("Step 1: Select Country")
    response = requests.get(f"{API_URL}/countries")
    if response.status_code == 200:
        countries = response.json()
        selected_country = st.selectbox("Select a Country", countries)
    else:
        st.error("Failed to fetch countries.")
        return
    st.subheader("Step 2: Select City")
    if selected_country:
        resp_cities = requests.post(f"{API_URL}/cities", json={"country": selected_country})
        if resp_cities.status_code == 200:
            city_list = resp_cities.json()
            selected_city = st.selectbox("Select a City", city_list)
        else:
            st.error("Failed to fetch cities.")
            return
    else:
        st.info("No country selected.")
        return
    st.subheader("Step 3: Select Category and Radius")
    cats = ["medical_tourism", "mice", "destination_weddings"]
    selected_category = st.selectbox("Select a Category", cats)
    radius = st.slider("Select Radius (meters)", 5000, 100000, 50000, step=5000)
    st.subheader("Step 4: Process Data")
    if st.button("Process"):
        with st.spinner("Processing..."):
            payload = {"city": selected_city, "category": selected_category, "radius": radius}
            resp_proc = requests.post(f"{API_URL}/process", json=payload)
            if resp_proc.status_code == 200:
                result = resp_proc.json()
                st.success("Data processed successfully!")
                st.markdown("### Download Files")
                st.markdown(f"[Download CSV]({result['csv_file']})", unsafe_allow_html=True)
                st.markdown(f"[Download GeoJSON]({result['geojson_file']})", unsafe_allow_html=True)
                st.markdown(f"[Download Plot]({result['plot_file']})", unsafe_allow_html=True)
                st.markdown(f"[Download Map]({result['map_file']})", unsafe_allow_html=True)
                st.markdown("### Generated Plot")
                if os.path.exists(result['plot_file']):
                    st.image(Image.open(result['plot_file']), caption="Generated Plot")
                st.markdown("### Interactive Map")
                if os.path.exists(result['map_file']):
                    try:
                        with open(result['map_file'], "r", encoding="utf-8") as map_file:
                            html_content = map_file.read()
                            components.html(html_content, height=600)
                    except Exception as e:
                        st.error(f"Error displaying map: {e}")
                try:
                    download_url = f"{API_URL}/download?file_path={result['csv_file']}"
                    csv_resp = requests.get(download_url)
                    if csv_resp.status_code == 200:
                        csv_str = csv_resp.content.decode('utf-8', errors='replace')
                        df = pd.read_csv(io.StringIO(csv_str))
                        st.session_state.city_data = df
                    else:
                        st.warning("CSV download failed.")
                except Exception as e:
                    st.warning(f"CSV retrieval error: {e}")
                if "recommendations" in result:
                    display_recommendations(result["recommendations"], "Recommended Spots")
            else:
                st.error(f"Error: {resp_proc.json().get('error', 'Unknown error')}")
    if st.session_state.city_data is not None and not st.session_state.city_data.empty:
        st.markdown("### City Data (Interactive Table)")
        df = st.session_state.city_data
        # Filter out rows with "Unnamed Location"
        df = df[df['name'] != "Unnamed Location"]
        row_max = len(df)
        rows_to_show = st.slider("Number of rows to display", 1, row_max, min(10, row_max))
        st.dataframe(df.head(rows_to_show))
        display_analytics(df, "City Features Distribution")

# ---------------------------
# Hotel Explorer
# ---------------------------
def show_hotel_explorer():
    st.header("Hotel Explorer")
    st.write("Search for hotels near a city or country.")
    st.subheader("Step 1: Select Country")
    resp = requests.get(f"{API_URL}/countries")
    if resp.status_code == 200:
        cty_list = resp.json()
        selected_country = st.selectbox("Select a Country (optional)", [""] + cty_list, index=0)
    else:
        st.error("Failed to fetch countries.")
        return
    st.subheader("Step 2: Select City")
    city_options = []
    if selected_country:
        r = requests.post(f"{API_URL}/cities", json={"country": selected_country})
        if r.status_code == 200:
            city_options = r.json()
    selected_city = st.selectbox("Select a City (optional)", [""] + city_options, index=0)
    st.subheader("Step 3: Search Hotels")
    radius = st.slider("Select Radius (meters)", 5000, 50000, 20000, step=5000)
    if st.button("Search Hotels"):
        with st.spinner("Searching..."):
            params = {"city": selected_city, "country": selected_country, "radius": radius}
            r_hotels = requests.get(f"{API_URL}/hotels/search", params=params)
            if r_hotels.status_code == 200:
                data = r_hotels.json()
                st.success(f"Found {data['count']} hotels.")
                if "data" in data:
                    st.session_state.hotel_data = pd.DataFrame(data["data"])
                if "map_content" in data and data["map_content"]:
                    st.markdown("### Hotel Map")
                    components.html(data["map_content"], height=600)
                if "recommendations" in data:
                    display_recommendations(data["recommendations"], "Recommended Hotels")
            else:
                st.error("Hotel search failed.")
    if st.session_state.hotel_data is not None and not st.session_state.hotel_data.empty:
        st.markdown("### Hotel Data (Interactive Table)")
        df = st.session_state.hotel_data
        # Filter out rows with "Unnamed Location"
        df = df[df['name'] != "Unnamed Location"]
        row_max = len(df)
        rows_to_show = st.slider("Number of rows to display", 1, row_max, min(10, row_max))
        st.dataframe(df.head(rows_to_show))

# ---------------------------
# Sightseeing Explorer
# ---------------------------
def show_sightseeing_explorer():
    st.header("Sightseeing Explorer")
    st.write("Search for sightseeing spots in a city or country.")
    st.subheader("Step 1: Select Country")
    resp = requests.get(f"{API_URL}/countries")
    if resp.status_code == 200:
        cty_list = resp.json()
        selected_country = st.selectbox("Select a Country (optional)", [""] + cty_list, index=0)
    else:
        st.error("Failed to fetch countries.")
        return
    st.subheader("Step 2: Select City")
    city_options = []
    if selected_country:
        r = requests.post(f"{API_URL}/cities", json={"country": selected_country})
        if r.status_code == 200:
            city_options = r.json()
    selected_city = st.selectbox("Select a City (optional)", [""] + city_options, index=0)
    st.subheader("Step 3: Search Sightseeing")
    radius = st.slider("Select Radius (meters)", 5000, 50000, 20000, step=5000)
    if st.button("Search Sightseeing"):
        with st.spinner("Searching..."):
            params = {"city": selected_city, "country": selected_country, "radius": radius}
            r_sight = requests.get(f"{API_URL}/sightseeing/search", params=params)
            if r_sight.status_code == 200:
                data = r_sight.json()
                st.success(f"Found {data['count']} sightseeing spots.")
                if "data" in data:
                    st.session_state.sightseeing_data = pd.DataFrame(data["data"])
                if "map_content" in data and data["map_content"]:
                    st.markdown("### Sightseeing Map")
                    components.html(data["map_content"], height=600)
                if "recommendations" in data:
                    display_recommendations(data["recommendations"], "Recommended Sightseeing Spots")
            else:
                st.error("Sightseeing search failed.")
    if st.session_state.sightseeing_data is not None and not st.session_state.sightseeing_data.empty:
        st.markdown("### Sightseeing Data (Interactive Table)")
        df = st.session_state.sightseeing_data
        # Filter out rows with "Unnamed Location"
        df = df[df['name'] != "Unnamed Location"]
        row_max = len(df)
        rows_to_show = st.slider("Number of rows to display", 1, row_max, min(10, row_max))
        st.dataframe(df.head(rows_to_show))

# ---------------------------
# Airport Explorer
# ---------------------------
def show_airport_explorer():
    st.header("Airport & Airfield Explorer")
    st.write("Search for airports and airfields near a city or country.")
    st.subheader("Step 1: Select Country")
    resp = requests.get(f"{API_URL}/countries")
    if resp.status_code == 200:
        cty_list = resp.json()
        selected_country = st.selectbox("Select a Country (optional)", [""] + cty_list, index=0)
    else:
        st.error("Failed to fetch countries.")
        return
    st.subheader("Step 2: Select City")
    city_options = []
    if selected_country:
        r = requests.post(f"{API_URL}/cities", json={"country": selected_country})
        if r.status_code == 200:
            city_options = r.json()
    selected_city = st.selectbox("Select a City (optional)", [""] + city_options, index=0)
    st.subheader("Step 3: Search Airports & Airfields")
    radius = st.slider("Select Radius (meters)", 5000, 50000, 20000, step=5000)
    if st.button("Search Airports"):
        with st.spinner("Searching..."):
            params = {"city": selected_city, "country": selected_country, "radius": radius}
            r_air = requests.get(f"{API_URL}/airports/search", params=params)
            if r_air.status_code == 200:
                data = r_air.json()
                st.success(f"Found {data['count']} airports/airfields.")
                if "map_content" in data and data["map_content"]:
                    st.markdown("### Airports Map")
                    components.html(data["map_content"], height=600)
                if "data" in data:
                    st.session_state.airport_data = pd.DataFrame(data["data"])
                    st.markdown("### Airports Data (Interactive Table)")
                    df = st.session_state.airport_data
                    # Filter out rows with "Unnamed Location"
                    df = df[df['name'] != "Unnamed Location"]
                    row_max = len(df)
                    rows_to_show = st.slider("Number of rows to display", 1, row_max, min(10, row_max))
                    st.dataframe(df.head(rows_to_show))
                if "recommendations" in data:
                    display_recommendations(data["recommendations"], "Recommended Airports/Airfields")
            else:
                st.error("Airport search failed.")

# ---------------------------
# Airline Explorer
# ---------------------------
def show_airline_explorer():
    st.header("Airline Explorer")
    st.write("Search for airlines near a city or country.")
    st.subheader("Step 1: Select Country")
    resp = requests.get(f"{API_URL}/countries")
    if resp.status_code == 200:
        cty_list = resp.json()
        selected_country = st.selectbox("Select a Country (optional)", [""] + cty_list, index=0)
    else:
        st.error("Failed to fetch countries.")
        return
    st.subheader("Step 2: Select City")
    city_options = []
    if selected_country:
        r = requests.post(f"{API_URL}/cities", json={"country": selected_country})
        if r.status_code == 200:
            city_options = r.json()
    selected_city = st.selectbox("Select a City (optional)", [""] + city_options, index=0)
    st.subheader("Step 3: Search Airlines")
    radius = st.slider("Select Radius (meters)", 5000, 50000, 20000, step=5000)
    if st.button("Search Airlines"):
        with st.spinner("Searching..."):
            params = {"city": selected_city, "country": selected_country, "radius": radius}
            r_airl = requests.get(f"{API_URL}/airlines/search", params=params)
            if r_airl.status_code == 200:
                data = r_airl.json()
                st.success(f"Found {data['count']} airlines.")
                if "map_content" in data and data["map_content"]:
                    st.markdown("### Airlines Map")
                    components.html(data["map_content"], height=600)
                if "data" in data:
                    st.session_state.airline_data = pd.DataFrame(data["data"])
                    st.markdown("### Airlines Data (Interactive Table)")
                    df = st.session_state.airline_data
                    # Filter out rows with "Unnamed Location"
                    df = df[df['name'] != "Unnamed Location"]
                    row_max = len(df)
                    rows_to_show = st.slider("Number of rows to display", 1, row_max, min(10, row_max))
                    st.dataframe(df.head(rows_to_show))
                if "recommendations" in data:
                    display_recommendations(data["recommendations"], "Recommended Airlines")
            else:
                st.error("Airline search failed.")

# ---------------------------
# Medical Tourism Explorer
# ---------------------------
def show_medical_explorer():
    st.header("Medical Tourism Explorer")
    st.write("Search for hospitals, clinics, and medical facilities near a city or country.")
    st.subheader("Step 1: Select Country")
    resp = requests.get(f"{API_URL}/countries")
    if resp.status_code == 200:
        countries = resp.json()
        selected_country = st.selectbox("Select a Country", [""] + countries, index=0)
    else:
        st.error("Failed to fetch countries.")
        return
    st.subheader("Step 2: Select City")
    city_options = []
    if selected_country:
        r = requests.post(f"{API_URL}/cities", json={"country": selected_country})
        if r.status_code == 200:
            city_options = r.json()
    selected_city = st.selectbox("Select a City", [""] + city_options, index=0)
    st.subheader("Step 3: Search Medical Facilities")
    radius = st.slider("Select Radius (meters)", 5000, 50000, 20000, step=5000)
    if st.button("Search Medical Facilities"):
        with st.spinner("Searching..."):
            params = {"city": selected_city, "country": selected_country, "radius": radius}
            r_med = requests.get(f"{API_URL}/medical/search", params=params)
            if r_med.status_code == 200:
                data = r_med.json()
                st.success(f"Found {data['count']} medical facilities.")
                if "map_content" in data and data["map_content"]:
                    st.markdown("### Medical Facilities Map")
                    components.html(data["map_content"], height=600)
                if "data" in data:
                    st.session_state.medical_data = pd.DataFrame(data["data"])
                    st.markdown("### Medical Facilities Data (Interactive Table)")
                    df = st.session_state.medical_data
                    # Filter out "Unnamed Location"
                    df = df[df['name'] != "Unnamed Location"]
                    row_max = len(df)
                    rows_to_show = st.slider("Number of rows to display", 1, row_max, min(10, row_max))
                    st.dataframe(df.head(rows_to_show))
                if "recommendations" in data:
                    display_recommendations(data["recommendations"], "Recommended Medical Facilities")
            else:
                st.error("Medical facility search failed.")

# ---------------------------
# MICE Explorer
# ---------------------------
def show_mice_explorer():
    st.header("MICE Explorer")
    st.write("Search for conference centres, exhibition halls, and event venues near a city or country.")
    st.subheader("Step 1: Select Country")
    resp = requests.get(f"{API_URL}/countries")
    if resp.status_code == 200:
        countries = resp.json()
        selected_country = st.selectbox("Select a Country", [""] + countries, index=0)
    else:
        st.error("Failed to fetch countries.")
        return
    st.subheader("Step 2: Select City")
    city_options = []
    if selected_country:
        r = requests.post(f"{API_URL}/cities", json={"country": selected_country})
        if r.status_code == 200:
            city_options = r.json()
    selected_city = st.selectbox("Select a City", [""] + city_options, index=0)
    st.subheader("Step 3: Search MICE Venues")
    radius = st.slider("Select Radius (meters)", 5000, 50000, 20000, step=5000)
    if st.button("Search MICE Venues"):
        with st.spinner("Searching..."):
            params = {"city": selected_city, "country": selected_country, "radius": radius}
            r_mice = requests.get(f"{API_URL}/mice/search", params=params)
            if r_mice.status_code == 200:
                data = r_mice.json()
                st.success(f"Found {data['count']} MICE venues.")
                if "map_content" in data and data["map_content"]:
                    st.markdown("### MICE Venues Map")
                    components.html(data["map_content"], height=600)
                if "data" in data:
                    st.session_state.mice_data = pd.DataFrame(data["data"])
                    st.markdown("### MICE Venues Data (Interactive Table)")
                    df = st.session_state.mice_data
                    # Filter out "Unnamed Location"
                    df = df[df['name'] != "Unnamed Location"]
                    row_max = len(df)
                    rows_to_show = st.slider("Number of rows to display", 1, row_max, min(10, row_max))
                    st.dataframe(df.head(rows_to_show))
                if "recommendations" in data:
                    display_recommendations(data["recommendations"], "Recommended MICE Venues")
            else:
                st.error("MICE venue search failed.")

if __name__ == "__main__":
    main()
