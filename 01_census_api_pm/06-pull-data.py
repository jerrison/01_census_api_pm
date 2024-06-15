import requests
import csv
import os

def fetch_data(token, datasetid, startdate, enddate, locationid, limit=1000):
    base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    headers = {
        'token': token
    }
    data = []
    offset = 0

    while True:
        params = {
            'datasetid': datasetid,
            'startdate': startdate,
            'enddate': enddate,
            'limit': limit,
            'offset': offset,
            'locationid': locationid
        }
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            break
        response_data = response.json()
        data.extend(response_data.get('results', []))
        if len(response_data.get('results', [])) < limit:
            break
        offset += limit

    return data

def save_data_to_csv(data, filename="data/data.csv"):
    if not data:
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Example usage
token = "UaOPgCYeQaneCdyXLracsJbpgUVQBXso"  # Replace with your actual token
datasetid = "GHCND"  # Replace with your desired dataset ID
startdate = "2023-01-02"  # Replace with your desired start date
enddate = "2023-01-10"  # Replace with your desired end date
locationid = "CITY:US060031"  # Replace with your desired location ID
data = fetch_data(token, datasetid, startdate, enddate, locationid)
save_data_to_csv(data)
