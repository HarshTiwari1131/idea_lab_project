import requests
from key import key  # Ensure the key is correctly imported
import json

def fetch_news():
    """Fetch news from the API."""
    api_address = f"http://newsapi.org/v2/top-headlines?country=in&apiKey={key}"
    
    try:
        response = requests.get(api_address)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()
        
        # Ensure 'articles' key exists and is a list
        if 'articles' not in json_data or not isinstance(json_data['articles'], list):
            print("No articles found in the response.")
            return []

        return json_data['articles']

    except requests.RequestException as e:
        print(f"HTTP Request error: {e}")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        return []

def news():
    """Generate a list of news headlines."""
    articles = fetch_news()
    
    # Check if articles list is not empty
    if not articles:
        return ["No news available."]

    arr = []
    for i in range(min(3, len(articles))):  # Ensure we only access valid indices
        arr.append(f"Number {i+1} --> {articles[i]['title']}.")

    return arr
