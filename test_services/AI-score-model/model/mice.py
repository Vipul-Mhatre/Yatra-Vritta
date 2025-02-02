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

# === FETCHING MICE-RELATED INDICATORS ===
world_bank_api_url = "http://api.worldbank.org/v2/country/{}/indicator/{}?format=json&mrv=1"

# Define MICE indicators dynamically
mice_indicators = {
    "IC.BUS.EASE.XQ": "Ease of Doing Business Score",
    "NY.GDP.PCAP.CD": "GDP per Capita (USD)",
    "IS.AIR.PSGR": "International Air Passengers",
    "ST.INT.ARVL": "Tourist Arrivals",
    "VC.IHR.PSRC.P5": "Safety Index (Homicide Rate)",
}

# Fetch data dynamically from the World Bank API
def fetch_mice_data(country_code):
    country_data = {"countrycode": country_code}
    for indicator, name in mice_indicators.items():
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
    time.sleep(0.001)  # Prevent API rate limiting
    return country_data

# Fetch data for all countries
mice_data = [fetch_mice_data(country) for country in unique_countries]
mice_df = pd.DataFrame(mice_data)

# Debug: Print sample API results
print("\n===== Sample Fetched Data from World Bank API =====")
print(mice_df.head(10))

# === MERGE MICE DATA WITH MAIN DATASET ===
merged_df = df.merge(mice_df, on="countrycode", how="left")

# ✅ **Ensure all indicator columns exist before imputation**
indicator_columns = list(mice_indicators.values())
for col in indicator_columns:
    if col not in merged_df.columns:
        merged_df[col] = None  # Create missing columns if they don't exist

# Debug: Print before imputation
print("\n===== Data Before KNN Imputation (Missing Values Present) =====")
print(merged_df[indicator_columns].isna().sum())

# === HANDLING MISSING VALUES DYNAMICALLY ===
knn_imputer = KNNImputer(n_neighbors=5)

# ✅ **Use correct column list for imputation**
imputed_values = knn_imputer.fit_transform(merged_df[indicator_columns])

# ✅ **Assign values correctly to prevent shape mismatch**
merged_df[indicator_columns] = imputed_values

# Debug: Print after imputation
print("\n===== Data After KNN Imputation (Missing Values Filled) =====")
print(pd.DataFrame(imputed_values, columns=indicator_columns).head(10))

print("✅ KNN Imputation Applied for Missing Values")

# === NORMALIZATION FOR FAIR RANKING ===
scaler = MinMaxScaler()

# ✅ **Ensure proper normalization of indicators**
merged_df[indicator_columns] = scaler.fit_transform(merged_df[indicator_columns])

# Debug: Print after normalization
print("\n===== Data After Min-Max Normalization =====")
print(merged_df[indicator_columns].head(10))

# === COMPUTING MICE SCORE ===
weights = {
    "Ease of Doing Business Score": 0.3,
    "GDP per Capita (USD)": 0.3,
    "International Air Passengers": 0.2,
    "Tourist Arrivals": 0.1,
    "Safety Index (Homicide Rate)": 0.1
}

# ✅ **Fix: Ensure correct weight application and MICE Score calculation**
merged_df["MICE Score"] = merged_df[list(weights.keys())].mul(pd.Series(weights)).sum(axis=1)

# Debug: Print computed MICE Scores
print("\n===== Computed MICE Scores Before Sorting =====")
print(merged_df[["countrycode", "name", "MICE Score"]].head(10))

# Sort results
merged_df = merged_df.sort_values("MICE Score", ascending=False)
merged_df.to_csv("mice_destination_ranking.csv", index=False)

# Display top-ranked MICE destinations
print("\n===== TOP 10 MICE DESTINATIONS =====")
print(merged_df[["countrycode", "name", "MICE Score"]].head(10))
