import requests
import csv
import os

def fetch_location_categories(token, limit=1000):
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/locationcategories"
    headers = {
        'token': token
    }
    location_categories = []
    offset = 0

    while True:
        params = {
            'limit': limit,
            'offset': offset
        }
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            break
        data = response.json()
        location_categories.extend(data.get('results', []))
        if len(data.get('results', [])) < limit:
            break
        offset += limit

    return location_categories

def save_location_categories_to_csv(location_categories, filename="data/location_categories.csv"):
    if not location_categories:
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    keys = location_categories[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(location_categories)

# Example usage
token = "UaOPgCYeQaneCdyXLracsJbpgUVQBXso"  # Replace with your actual token
location_categories = fetch_location_categories(token)
save_location_categories_to_csv(location_categories)

