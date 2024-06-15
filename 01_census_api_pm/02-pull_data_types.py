import requests
import csv
import os

def fetch_data_types(token, limit=1000):
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/datatypes"
    headers = {
        'token': token
    }
    data_types = []
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
        data_types.extend(data.get('results', []))
        if len(data.get('results', [])) < limit:
            break
        offset += limit

    return data_types

def save_data_types_to_csv(data_types, filename="data/data_types.csv"):
    if not data_types:
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    keys = data_types[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data_types)

# Example usage
token = "UaOPgCYeQaneCdyXLracsJbpgUVQBXso"  # Replace with your actual token
data_types = fetch_data_types(token)
save_data_types_to_csv(data_types)

