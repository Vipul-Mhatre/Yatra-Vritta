import pandas as pd
import requests
import time
from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression

# Load the CSV file
file_path = r"C:\Algo_Master\project\complete_city_details_geonamescache.csv"  # Ensure correct path
df = pd.read_csv(file_path)

# Extract unique country codes
unique_countries = df["countrycode"].unique()
print(f"Total Unique Countries Found: {len(unique_countries)}\n")

# === FETCHING HEALTHCARE & ECONOMIC DATA (WORLD BANK) ===
world_bank_api_url = "http://api.worldbank.org/v2/country/{}/indicator/{}?format=json&mrv=1"

# Define indicators for Medical Tourism
indicators = {
    "SH.MED.BEDS.ZS": "Hospital Beds per 1,000",
    "SH.XPD.CHEX.PC.CD": "Health Spending per Capita (USD)",
    "NY.GDP.PCAP.CD": "GDP per Capita (USD)",
    "ST.INT.ARVL": "Tourist Arrivals per Year",
}

# Function to fetch World Bank data dynamically
def fetch_world_bank_data(country_code):
    country_data = {"countrycode": country_code}
    for indicator, name in indicators.items():
        try:
            url = world_bank_api_url.format(country_code.lower(), indicator)
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200 and len(data) > 1 and data[1]:
                value = data[1][0].get("value", None)
                country_data[name] = value
            else:
                country_data[name] = None
        except Exception as e:
            print(f"Error fetching {name} for {country_code}: {str(e)}")
            country_data[name] = None
    print(f"World Bank Data for {country_code}: {country_data}")  # Debug Output
    time.sleep(0.5)  # Prevent API rate limiting
    return country_data

# Fetch World Bank data dynamically
world_bank_data = [fetch_world_bank_data(country) for country in unique_countries]
wb_df = pd.DataFrame(world_bank_data)

# Merge World Bank data with the dataset
merged_df = df.merge(wb_df, on="countrycode", how="left")

# ✅ **Fix 1: Ensure all indicator columns exist before imputation**
indicator_columns = list(indicators.values())
for col in indicator_columns:
    if col not in merged_df.columns:
        merged_df[col] = None  # Create missing columns if they don't exist

# === HANDLE MISSING VALUES DYNAMICALLY ===

# 1️⃣ **K-Nearest Neighbors (KNN) Imputation**
knn_imputer = KNNImputer(n_neighbors=5)

# ✅ **Fix 2: Use correct column list for imputation**
imputed_values = knn_imputer.fit_transform(merged_df[indicator_columns])

# ✅ **Fix 3: Assign values correctly to prevent shape mismatch**
merged_df[indicator_columns] = imputed_values
print("✅ KNN Imputation Applied for Missing Values")

# 2️⃣ **Regression-Based Imputation**
for col in indicator_columns:
    missing_rows = merged_df[col].isna()
    
    if missing_rows.sum() > 0:  # If there are missing values
        train_data = merged_df[~missing_rows]  # Rows with values
        test_data = merged_df[missing_rows]  # Rows without values
        
        # Ensure we don't use the target column in predictors
        X_train = train_data.drop(columns=indicator_columns)
        y_train = train_data[col]
        
        if not y_train.isna().all():  # Avoid fitting when no data is available
            reg = LinearRegression()
            reg.fit(X_train, y_train)
            merged_df.loc[missing_rows, col] = reg.predict(test_data.drop(columns=indicator_columns))
        
print("✅ Regression-Based Imputation Applied for Missing Values")

# 3️⃣ **Interpolation for Time-Series Data**
merged_df[indicator_columns] = merged_df[indicator_columns].interpolate(method='linear', limit_direction='forward')
print("✅ Interpolation Applied for Time-Series Missing Values")

# === CALCULATE MEDICAL TOURISM SCORE ===
weights = {
    "Hospital Beds per 1,000": 0.4,
    "Health Spending per Capita (USD)": 0.3,
    "GDP per Capita (USD)": 0.2,
    "Tourist Arrivals per Year": 0.1
}

# Normalize values dynamically
for column in weights.keys():
    if column in merged_df.columns:
        merged_df[column] = (merged_df[column] - merged_df[column].min()) / (merged_df[column].max() - merged_df[column].min())

# Compute the final Medical Tourism Score
merged_df["Medical Tourism Score"] = merged_df[list(weights.keys())].mul(pd.Series(weights)).sum(axis=1)

# Sort and export the results
merged_df = merged_df.sort_values("Medical Tourism Score", ascending=False)
merged_df.to_csv("enhanced_medical_tourism_analysis.csv", index=False)

# Display top-ranked medical tourism countries
print("\n===== TOP 10 MEDICAL TOURISM DESTINATIONS =====")
print(merged_df[["countrycode", "name", "Medical Tourism Score"]].head(10))
