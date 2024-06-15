import requests
import csv
import os

def fetch_stations(token, locationid=None, limit=1000):
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/stations"
    headers = {
        'token': token
    }
    stations = []
    offset = 0

    while True:
        params = {
            'limit': limit,
            'offset': offset
        }
        if locationid:
            params['locationid'] = locationid
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            break
        data = response.json()
        stations.extend(data.get('results', []))
        if len(data.get('results', [])) < limit:
            break
        offset += limit

    return stations

def save_stations_to_csv(stations, filename="data/stations.csv"):
    if not stations:
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    keys = stations[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(stations)

# Example usage
token = "UaOPgCYeQaneCdyXLracsJbpgUVQBXso"  # Replace with your actual token
locationid = "CITY:US060031"  # Replace with your actual locationid if needed
stations = fetch_stations(token, locationid)
save_stations_to_csv(stations)
