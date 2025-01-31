import geonamescache
import csv

# Initialize geonamescache
gc = geonamescache.GeonamesCache()
cities = gc.get_cities()
countries = gc.get_countries()

# Extract and print city and country data
city_coords = []
for code, details in cities.items():
    # Create a dictionary for the current city
    city_data = {
        'City': details['name'],
        'Country': countries[details['countrycode']]['name'] if details['countrycode'] in countries else 'Unknown',
        'Latitude': details['latitude'],
        'Longitude': details['longitude']
    }
    city_coords.append(city_data)

    # Print intermediate city data
    print(city_data)

# Save to CSV
csv_file = "cities_lat_long_geonamescache_with_countries.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['City', 'Country', 'Latitude', 'Longitude'])
    writer.writeheader()
    writer.writerows(city_coords)

print(f"City data with countries saved to {csv_file}")
