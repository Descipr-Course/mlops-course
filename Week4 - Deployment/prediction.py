import requests

nyc_test_data = {'PU_DO': '161_74', 'trip_distance': 3.7}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=nyc_test_data)
print(response.json())