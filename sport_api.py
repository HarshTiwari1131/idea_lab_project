# import requests

# def fetch_sports_data(endpoint, params):
#     url = f"https://actual-sports-api.com/{endpoint}"
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()  # Raise an HTTPError for bad responses
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching data: {e}")

# endpoint = "match-data"
# params = {
#     "league": "NBA",
#     "season": "2024",
#     "apikey": "3"
# }

# data = fetch_sports_data(endpoint, params)
# print(data)


import requests

def fetch_sports_data(endpoint, params=None):
    url = f"https://www.thesportsdb.com/api/v1/json/3/{endpoint}"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

endpoint = "searchteams.php"
params = {
    "t": "Arsenal"
}

data = fetch_sports_data(endpoint, params)
print(data)
