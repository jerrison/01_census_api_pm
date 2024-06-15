import requests
import csv
import os

def fetch_datasets(token, limit=1000):
    base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets"
    headers = {
        'token': token
    }
    datasets = []
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
        datasets.extend(data.get('results', []))
        if len(data.get('results', [])) < limit:
            break
        offset += limit

    return datasets

def save_to_csv(datasets, filename="data/datasets.csv"):
    if not datasets:
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    keys = datasets[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(datasets)

# Example usage
token = "UaOPgCYeQaneCdyXLracsJbpgUVQBXso"  # Replace with your actual token
datasets = fetch_datasets(token)
save_to_csv(datasets)


