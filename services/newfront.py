import streamlit as st
import requests
import os
from PIL import Image
import streamlit.components.v1 as components
import pandas as pd
import io

# Flask API base URL
API_URL = "http://127.0.0.1:5000"

# --- Initialize session state for stored DataFrames ---
if "city_data" not in st.session_state:
    st.session_state.city_data = None

if "hotel_data" not in st.session_state:
    st.session_state.hotel_data = None

if "sightseeing_data" not in st.session_state:
    st.session_state.sightseeing_data = None

def main():
    st.title("City Feature Explorer & More")

    page = st.sidebar.selectbox(
        "Select a Page",
        (
            "City Feature Explorer",
            "Hotel Explorer",
            "Sightseeing Explorer",
        )
    )

    if page == "City Feature Explorer":
        show_city_feature_explorer()
    elif page == "Hotel Explorer":
        show_hotel_explorer()
    else:
        show_sightseeing_explorer()

# ----------------------------------------------------------------------
#  CITY FEATURE EXPLORER
# ----------------------------------------------------------------------
def show_city_feature_explorer():
    """
    Existing City Feature Explorer Page.
    Uses POST /process to fetch CSV/GeoJSON/Plot/Map,
    then optionally reads the CSV to store in session state as a DataFrame.
    """
    st.header("City Feature Explorer")
    st.write("Explore features of a city based on different categories using Overpass API.")

    # Step 1: Get Countries
    st.subheader("Step 1: Select Country")
    response = requests.get(f"{API_URL}/countries")
    if response.status_code == 200:
        countries = response.json()
        selected_country = st.selectbox("Select a Country", countries)
    else:
        st.error("Failed to fetch countries.")
        return

    # Step 2: Get Cities
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

    # Step 3: Select Category & Radius
    st.subheader("Step 3: Select Category and Radius")
    categories = ["medical_tourism", "mice", "destination_weddings"]
    selected_category = st.selectbox("Select a Category", categories)
    radius = st.slider("Select Radius (meters)", min_value=5000, max_value=100000, value=50000, step=5000)

    # Step 4: Process Data (POST /process)
    st.subheader("Step 4: Process Data")
    if st.button("Process"):
        with st.spinner("Processing..."):
            payload = {
                "city": selected_city,
                "category": selected_category,
                "radius": radius
            }
            resp_proc = requests.post(f"{API_URL}/process", json=payload)
            if resp_proc.status_code == 200:
                result = resp_proc.json()
                st.success("Data processed successfully!")

                # Show various download links
                st.subheader("Download Files")
                st.markdown(f"[Download CSV]({result['csv_file']})", unsafe_allow_html=True)
                st.markdown(f"[Download GeoJSON]({result['geojson_file']})", unsafe_allow_html=True)
                st.markdown(f"[Download Plot]({result['plot_file']})", unsafe_allow_html=True)
                st.markdown(f"[Download Map]({result['map_file']})", unsafe_allow_html=True)

                # Display plot
                st.subheader("Plot")
                plot_image_path = result['plot_file']
                if os.path.exists(plot_image_path):
                    st.image(Image.open(plot_image_path), caption="Generated Plot")

                # Display map
                st.subheader("Map")
                map_file_path = result['map_file']
                if os.path.exists(map_file_path):
                    try:
                        with open(map_file_path, "r", encoding="utf-8") as map_file:
                            html_content = map_file.read()
                            components.html(html_content, height=600)
                    except Exception as e:
                        st.error(f"Error displaying the map: {e}")

                # Optionally, read the CSV from the backend's file path
                # We'll call the /download endpoint to get the CSV content.
                csv_file_server_path = result["csv_file"]  # e.g. "./output/medical_tourism_CityName.csv"
                download_url = f"{API_URL}/download?file_path={csv_file_server_path}"
                try:
                    csv_resp = requests.get(download_url)
                    if csv_resp.status_code == 200:
                        # Parse CSV into a DataFrame
                        csv_str = csv_resp.content.decode('utf-8', errors='replace')
                        df_city = pd.read_csv(io.StringIO(csv_str))
                        # Store in session state
                        st.session_state.city_data = df_city
                    else:
                        st.warning("Could not download the CSV file from the server.")
                except Exception as e:
                    st.warning(f"Failed to retrieve CSV from server: {e}")

            else:
                st.error(f"Error: {resp_proc.json().get('error', 'Unknown error occurred')}")

    # If we have city_data stored, show it
    if st.session_state.city_data is not None and not st.session_state.city_data.empty:
        st.subheader("City Data (Interactive Table)")
        df_city = st.session_state.city_data
        # Let user pick number of rows to display
        row_max = len(df_city)
        rows_to_show = st.slider("Number of rows to display", min_value=1, max_value=row_max, value=min(10, row_max))
        st.dataframe(df_city.head(rows_to_show))

# ----------------------------------------------------------------------
#  HOTEL EXPLORER
# ----------------------------------------------------------------------
def show_hotel_explorer():
    st.header("Hotel Explorer")
    st.write("Search for hotels near a city or country using Overpass API.")

    # 1) Select Country
    st.subheader("Step 1: Select Country")
    resp_cty = requests.get(f"{API_URL}/countries")
    if resp_cty.status_code == 200:
        cty_list = resp_cty.json()
        selected_country = st.selectbox("Select a Country (optional)", [""] + cty_list, index=0)
    else:
        st.error("Failed to fetch countries.")
        return

    # 2) Select City
    st.subheader("Step 2: Select City")
    city_options = []
    if selected_country:
        resp_cities = requests.post(f"{API_URL}/cities", json={"country": selected_country})
        if resp_cities.status_code == 200:
            city_options = resp_cities.json()

    selected_city = st.selectbox("Select a City (optional)", [""] + city_options, index=0)

    # 3) Search
    st.subheader("Step 3: Search Hotels")
    radius_hotel = st.slider("Select Radius (in meters)", 5000, 50000, 20000, step=5000)

    if st.button("Search Hotels"):
        with st.spinner("Searching..."):
            params = {
                "city": selected_city,
                "country": selected_country,
                "radius": radius_hotel
            }
            r_hotels = requests.get(f"{API_URL}/hotels/search", params=params)

            if r_hotels.status_code == 200:
                data = r_hotels.json()
                st.success(f"Found {data['count']} hotels.")

                # Save the data to session state
                if "data" in data and isinstance(data["data"], list):
                    st.session_state.hotel_data = pd.DataFrame(data["data"])
                else:
                    st.session_state.hotel_data = None

                # Show map
                if "map_content" in data and data["map_content"]:
                    st.subheader("Hotel Map")
                    components.html(data["map_content"], height=600)

            else:
                st.error("Failed to fetch hotels.")

    # Display stored data
    if st.session_state.hotel_data is not None and not st.session_state.hotel_data.empty:
        st.subheader("Hotel Data (Interactive Table)")
        df_hotel = st.session_state.hotel_data
        row_max = len(df_hotel)
        rows_to_show = st.slider("Number of rows to display", 1, row_max, min(10, row_max))
        st.dataframe(df_hotel.head(rows_to_show))

# ----------------------------------------------------------------------
#  SIGHTSEEING EXPLORER
# ----------------------------------------------------------------------
def show_sightseeing_explorer():
    st.header("Sightseeing Explorer")
    st.write("Search for sightseeing spots in a city or country.")

    # 1) Country
    st.subheader("Step 1: Select Country")
    resp_cnt = requests.get(f"{API_URL}/countries")
    if resp_cnt.status_code == 200:
        cty_list = resp_cnt.json()
        selected_country = st.selectbox("Select a Country (optional)", [""] + cty_list, index=0)
    else:
        st.error("Failed to fetch countries.")
        return

    # 2) City
    st.subheader("Step 2: Select City")
    city_options = []
    if selected_country:
        r_cities = requests.post(f"{API_URL}/cities", json={"country": selected_country})
        if r_cities.status_code == 200:
            city_options = r_cities.json()

    selected_city = st.selectbox("Select a City (optional)", [""] + city_options, index=0)

    # 3) Radius & Search
    st.subheader("Step 3: Select Radius (in meters)")
    radius_sight = st.slider("Radius", 5000, 50000, 20000, step=5000)

    if st.button("Search Sightseeing"):
        with st.spinner("Searching..."):
            params = {
                "city": selected_city,
                "country": selected_country,
                "radius": radius_sight
            }
            r_sight = requests.get(f"{API_URL}/sightseeing/search", params=params)
            if r_sight.status_code == 200:
                data = r_sight.json()
                st.success(f"Found {data['count']} sightseeing spots.")

                # Save the data to session state
                if "data" in data and isinstance(data["data"], list):
                    st.session_state.sightseeing_data = pd.DataFrame(data["data"])
                else:
                    st.session_state.sightseeing_data = None

                # Show map
                if "map_content" in data and data["map_content"]:
                    st.subheader("Sightseeing Map")
                    components.html(data["map_content"], height=600)
            else:
                st.error("Failed to fetch sightseeing spots.")

    # Display DataFrame
    if st.session_state.sightseeing_data is not None and not st.session_state.sightseeing_data.empty:
        st.subheader("Sightseeing Data (Interactive Table)")
        df_sight = st.session_state.sightseeing_data
        row_max = len(df_sight)
        rows_to_show = st.slider("Number of rows to display", 1, row_max, min(10, row_max))
        st.dataframe(df_sight.head(rows_to_show))

# ----------------------------------------------------------------------
#  ENTRY POINT
# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
