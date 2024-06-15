import requests
import csv
import os

def fetch_locations(token, limit=1000):
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/locations"
    headers = {
        'token': token
    }
    locations = []
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
        locations.extend(data.get('results', []))
        if len(data.get('results', [])) < limit:
            break
        offset += limit

    return locations

def save_locations_to_csv(locations, filename="data/locations.csv"):
    if not locations:
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    keys = locations[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(locations)

# Example usage
token = "UaOPgCYeQaneCdyXLracsJbpgUVQBXso"  # Replace with your actual token
locations = fetch_locations(token)
save_locations_to_csv(locations)

