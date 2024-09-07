import requests
from key import key  # Ensure the key is correctly imported
import json

def fetch_news(country='us',category = 'general'):
    """Fetch news from the API based on user input."""
    api_address = f"http://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={key}"
    
    try:
        response = requests.get(api_address)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()

        # Debug: Print the raw JSON response
        print("Raw JSON response:", json.dumps(json_data, indent=2))
        
        # Ensure 'articles' key exists and is a list
        if not json_data.get('articles') or not isinstance(json_data['articles'], list):
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
    """Generate a list of news headlines based on user input."""
    # Ask user for input
    country = 'us'
    category = 'general' #'technology' 'business' input("Enter the news category (e.g., 'general', 'technology', 'business'): ").strip().lower()

    articles = fetch_news(country, category)
    
    # Check if articles list is not empty
    if not articles:
        return ["No news available."]

    arr = []
    for i in range(min(3, len(articles))):  # Ensure we only access valid indices
        title = articles[i].get('title', 'No title available')
        arr.append(f"Number {i + 1} --> {title}.")

    return arr

if __name__ == "__main__":
    headlines = news()
    for headline in headlines:
        print(headline)
