import requests
import csv
import os

def fetch_data_categories(token, limit=1000):
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/datacategories"
    headers = {
        'token': token
    }
    data_categories = []
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
        data_categories.extend(data.get('results', []))
        if len(data.get('results', [])) < limit:
            break
        offset += limit

    return data_categories

def save_data_categories_to_csv(data_categories, filename="data/data_categories.csv"):
    if not data_categories:
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    keys = data_categories[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data_categories)

# Example usage
token = "UaOPgCYeQaneCdyXLracsJbpgUVQBXso"  # Replace with your actual token
data_categories = fetch_data_categories(token)
save_data_categories_to_csv(data_categories)

