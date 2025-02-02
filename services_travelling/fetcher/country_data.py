import pandas as pd
import requests

# Load the CSV file
file_path = r"C:\Algo_Master\project\complete_city_details_geonamescache.csv"  # Ensure correct file path
df = pd.read_csv(file_path)

# Extract unique country codes from the dataset
unique_countries = df["countrycode"].unique()

# Define World Bank API base URL
world_bank_api_url = "http://api.worldbank.org/v2/country/{}/indicator/{}?format=json&date=2023"

# Define indicators to fetch from World Bank API
indicators = {
    "SH.MED.BEDS.ZS": "Hospital Beds per 1,000",
    "SH.XPD.CHEX.PC.CD": "Health Spending per Capita (USD)",
    "NY.GDP.PCAP.CD": "GDP per Capita (USD)",
    "ST.INT.ARVL": "Tourist Arrivals per Year",
}

# Function to fetch data for a given country code
def fetch_world_bank_data(country_code):
    country_data = {"countrycode": country_code}
    for indicator, name in indicators.items():
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
            country_data[name] = None
    return country_data

# Fetch World Bank data for all unique countries
world_bank_data = [fetch_world_bank_data(country) for country in unique_countries]

# Convert World Bank data to DataFrame
wb_df = pd.DataFrame(world_bank_data)

# Merge World Bank data with Geonamescache dataset
merged_df = df.merge(wb_df, on="countrycode", how="left")

# Define weights for Medical Tourism Score
weights = {
    "Hospital Beds per 1,000": 0.3,
    "Health Spending per Capita (USD)": 0.4,
    "GDP per Capita (USD)": 0.2,
    "Tourist Arrivals per Year": 0.1,
}

# Normalize values and compute Medical Tourism Score
for column in weights.keys():
    if column in merged_df.columns:
        merged_df[column] = (merged_df[column] - merged_df[column].min()) / (merged_df[column].max() - merged_df[column].min())
        print(merged_df)

merged_df["Medical Tourism Score"] = merged_df[list(weights.keys())].mul(pd.Series(weights)).sum(axis=1)

# Sort countries by Medical Tourism Score
merged_df = merged_df.sort_values("Medical Tourism Score", ascending=False)

# Save to CSV file
output_file = "medical_tourism_analysis.csv"
merged_df.to_csv(output_file, index=False)
print(f"Medical tourism dataset saved to '{output_file}'.")

# Display top 10 countries with the best Medical Tourism Score
print(merged_df[["countrycode", "name", "Medical Tourism Score"]].head(10))
