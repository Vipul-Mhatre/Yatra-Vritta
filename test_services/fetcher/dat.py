#!/usr/bin/env python
"""
country_data_automation.py

This script fetches complete country data by:
  1. Using the REST Countries API to get a list of all countries and all available details.
  2. Fetching GDP per capita (indicator: NY.GDP.PCAP.CD) and population (indicator: SP.POP.TOTL)
     time series data from the World Bank using each country's ISO2 code.
  3. Saving the results into CSV files:
       - all_country_info.csv         : Complete details (flattened) from REST Countries.
       - gdp_per_capita.csv             : Full time series data for GDP per capita.
       - population.csv                 : Full time series data for population.
       - combined_country_info.csv      : Combined data merging country info with latest GDP & population.
       
Dependencies:
    pip install requests pandas-datareader pandas
"""

import datetime
import requests
import pandas as pd
import pandas_datareader.data as web

# ---------------------------------------------------
# Step 1: Fetch Complete Country Data from REST Countries API
# ---------------------------------------------------

def get_country_list():
    """
    Fetch complete country data from the REST Countries API.
    
    Returns:
        list of dict: Each dictionary contains all details about a country.
                      Only countries with both a common name and an ISO2 code (cca2) are included.
    """
    url = "https://restcountries.com/v3.1/all"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Only include countries that have a common name and a 2-letter ISO code
            countries = [country for country in data
                         if country.get('name', {}).get('common') and country.get('cca2')]
            return countries
        else:
            print(f"Error fetching country list: HTTP {response.status_code}")
            return []
    except Exception as e:
        print("Exception while fetching country list:", e)
        return []

# ---------------------------------------------------
# Step 2: Fetch Economic Data from World Bank
# ---------------------------------------------------

def get_gdp_per_capita_by_code(iso2_code, start_year=2000, end_year=2020):
    """
    Fetch GDP per capita (current US$) time series data for a given ISO2 country code from the World Bank.
    
    Parameters:
        iso2_code (str): Two-letter ISO country code.
        start_year (int): Start year for the time series.
        end_year (int): End year for the time series.
        
    Returns:
        pandas.DataFrame or None: DataFrame with columns 'date' and 'gdp_per_capita', plus a 'cca2' column.
    """
    try:
        start = datetime.datetime(start_year, 1, 1)
        end = datetime.datetime(end_year, 12, 31)
        data = web.DataReader("NY.GDP.PCAP.CD", "wb", start, end, country=iso2_code)
        if data is not None and not data.empty:
            data = data.reset_index()  # Bring the 'date' (year) into a column
            # Rename the indicator column for clarity
            if "NY.GDP.PCAP.CD" in data.columns:
                data = data.rename(columns={"NY.GDP.PCAP.CD": "gdp_per_capita"})
            else:
                cols = list(data.columns)
                if "date" in cols:
                    cols.remove("date")
                if cols:
                    data = data.rename(columns={cols[0]: "gdp_per_capita"})
            # Add ISO2 code for later merging
            data["cca2"] = iso2_code
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching GDP data for {iso2_code}: {e}")
        return None

def get_population_by_code(iso2_code, start_year=2000, end_year=2020):
    """
    Fetch total population time series data for a given ISO2 country code from the World Bank.
    
    Parameters:
        iso2_code (str): Two-letter ISO country code.
        start_year (int): Start year for the time series.
        end_year (int): End year for the time series.
        
    Returns:
        pandas.DataFrame or None: DataFrame with columns 'date' and 'population', plus a 'cca2' column.
    """
    try:
        start = datetime.datetime(start_year, 1, 1)
        end = datetime.datetime(end_year, 12, 31)
        data = web.DataReader("SP.POP.TOTL", "wb", start, end, country=iso2_code)
        if data is not None and not data.empty:
            data = data.reset_index()
            if "SP.POP.TOTL" in data.columns:
                data = data.rename(columns={"SP.POP.TOTL": "population"})
            else:
                cols = list(data.columns)
                if "date" in cols:
                    cols.remove("date")
                if cols:
                    data = data.rename(columns={cols[0]: "population"})
            data["cca2"] = iso2_code
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching population data for {iso2_code}: {e}")
        return None

# ---------------------------------------------------
# Step 3: Automation & Data Aggregation
# ---------------------------------------------------

def main():
    START_YEAR = 2000
    END_YEAR = 2020

    print("Fetching complete country data from REST Countries API...")
    countries = get_country_list()
    print(f"Total countries fetched: {len(countries)}")

    # Flatten the complete country info using pandas.json_normalize
    basic_info_df = pd.json_normalize(countries)
    basic_info_df.to_csv("all_country_info.csv", index=False)
    print("Saved complete country info to all_country_info.csv")

    # Prepare lists for economic data
    gdp_list = []
    population_list = []
    
    total = len(countries)
    for idx, country in enumerate(countries, start=1):
        # Use the common name and ISO2 code from the REST Countries data
        name = country.get('name', {}).get('common', 'Unknown')
        iso2 = country.get('cca2')
        print(f"Processing {idx}/{total}: {name} (ISO2: {iso2})")
        
        # Fetch GDP per capita data using the ISO2 code
        gdp_data = get_gdp_per_capita_by_code(iso2, START_YEAR, END_YEAR)
        if gdp_data is not None:
            # Optionally add the country name for clarity
            gdp_data["country"] = name
            gdp_list.append(gdp_data)
        
        # Fetch population data using the ISO2 code
        pop_data = get_population_by_code(iso2, START_YEAR, END_YEAR)
        if pop_data is not None:
            pop_data["country"] = name
            population_list.append(pop_data)
    
    # Concatenate economic data if available
    if gdp_list:
        gdp_df = pd.concat(gdp_list, ignore_index=True)
        gdp_df.to_csv("gdp_per_capita.csv", index=False)
        print("Saved GDP per capita data to gdp_per_capita.csv")
    else:
        gdp_df = pd.DataFrame()
    
    if population_list:
        population_df = pd.concat(population_list, ignore_index=True)
        population_df.to_csv("population.csv", index=False)
        print("Saved population data to population.csv")
    else:
        population_df = pd.DataFrame()
    
    # Create a combined DataFrame merging the complete country info with the latest economic data
    combined_df = basic_info_df.copy()
    
    if not gdp_df.empty:
        # For each country, get the most recent GDP data (sort by 'date')
        gdp_latest = gdp_df.sort_values("date").groupby("cca2").last().reset_index()
        gdp_latest = gdp_latest.rename(columns={"date": "gdp_year"})
        combined_df = pd.merge(combined_df, gdp_latest[["cca2", "gdp_per_capita", "gdp_year"]],
                               on="cca2", how="left")
    
    if not population_df.empty:
        # For each country, get the most recent population data
        pop_latest = population_df.sort_values("date").groupby("cca2").last().reset_index()
        pop_latest = pop_latest.rename(columns={"date": "pop_year"})
        combined_df = pd.merge(combined_df, pop_latest[["cca2", "population", "pop_year"]],
                               on="cca2", how="left")
    
    combined_df.to_csv("combined_country_info.csv", index=False)
    print("Saved combined country info to combined_country_info.csv")

if __name__ == "__main__":
    main()
