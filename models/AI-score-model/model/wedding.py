import pandas as pd
import requests
import time
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler

# Load country dataset
file_path = r"C:\Algo_Master\project\complete_city_details_geonamescache.csv"  # Ensure correct path
df = pd.read_csv(file_path)

# Extract unique country codes
unique_countries = df["countrycode"].unique()
print(f"Total Unique Countries Found: {len(unique_countries)}\n")

# === FETCHING DESTINATION WEDDING INDICATORS ===
world_bank_api_url = "http://api.worldbank.org/v2/country/{}/indicator/{}?format=json&mrv=1"

# Define Destination Wedding indicators dynamically
wedding_indicators = {
    "ST.INT.ARVL": "Tourist Arrivals (millions)",  # Scenic Beauty & Popularity
    "IC.BUS.EASE.XQ": "Ease of Business Score",  # Marriage Law Simplicity
    "NY.GDP.PCAP.CD": "GDP per Capita (USD)",  # Luxury Infrastructure Proxy
    "IS.AIR.PSGR": "International Air Passengers",  # Travel Connectivity
    "VC.IHR.PSRC.P5": "Safety Index (Low Crime Rate)",  # Safety Consideration
}

# Fetch data dynamically from the World Bank API
def fetch_wedding_data(country_code):
    country_data = {"countrycode": country_code}
    for indicator, name in wedding_indicators.items():
        try:
            url = world_bank_api_url.format(country_code.lower(), indicator)
            response = requests.get(url)
            data = response.json()
            print(data)
            if response.status_code == 200 and len(data) > 1 and data[1]:
                value = data[1][0].get("value", None)
                country_data[name] = value
            else:
                country_data[name] = None
        except Exception as e:
            print(f"Error fetching {name} for {country_code}: {str(e)}")
            country_data[name] = None
    time.sleep(0.5)  # Prevent API rate limiting
    return country_data

# Fetch data for all countries
wedding_data = [fetch_wedding_data(country) for country in unique_countries]
wedding_df = pd.DataFrame(wedding_data)

# === MERGE WEDDING DATA WITH MAIN DATASET ===
merged_df = df.merge(wedding_df, on="countrycode", how="left")

# ✅ **Ensure all indicator columns exist before imputation**
indicator_columns = list(wedding_indicators.values())
for col in indicator_columns:
    if col not in merged_df.columns:
        merged_df[col] = None  # Create missing columns if they don't exist

# === HANDLING MISSING VALUES DYNAMICALLY ===
knn_imputer = KNNImputer(n_neighbors=5)

# ✅ **Use correct column list for imputation**
imputed_values = knn_imputer.fit_transform(merged_df[indicator_columns])

# ✅ **Assign values correctly to prevent shape mismatch**
merged_df[indicator_columns] = imputed_values
print("✅ KNN Imputation Applied for Missing Values")

# === NORMALIZATION FOR FAIR RANKING ===
scaler = MinMaxScaler()

# ✅ **Ensure proper normalization of indicators**
merged_df[indicator_columns] = scaler.fit_transform(merged_df[indicator_columns])

# === COMPUTING DESTINATION WEDDING SCORE ===
weights = {
    "Tourist Arrivals (millions)": 0.3,  # Scenic Beauty & Popularity
    "Ease of Business Score": 0.2,  # Ease of Legal Marriage
    "GDP per Capita (USD)": 0.2,  # Luxury Infrastructure Proxy
    "International Air Passengers": 0.2,  # Accessibility
    "Safety Index (Low Crime Rate)": 0.1,  # Safety
}

# ✅ **Ensure correct weight application and Destination Wedding Score calculation**
merged_df["Destination Wedding Score"] = merged_df[list(weights.keys())].mul(pd.Series(weights)).sum(axis=1)

# Sort results
merged_df = merged_df.sort_values("Destination Wedding Score", ascending=False)
merged_df.to_csv("destination_wedding_ranking.csv", index=False)

# Display top-ranked Wedding Destinations
print("\n===== TOP 10 DESTINATION WEDDING LOCATIONS =====")
print(merged_df[["countrycode", "name", "Destination Wedding Score"]].head(10))
