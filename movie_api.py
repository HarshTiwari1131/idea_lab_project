import requests

API_KEY = '0ded20ddad3d9f64aa59810e6b60db64'
BASE_URL = 'https://api.themoviedb.org/3'

def get_movie_details(movie_name):
    """Fetch movie details from TMDB API based on the movie name."""
    try:
        # Make a request to search for the movie
        response = requests.get(f"{BASE_URL}/search/movie", params={
            'api_key': API_KEY,
            'query': movie_name
        })
        response.raise_for_status()
        data = response.json()

        # Check if any movie is found
        if data['results']:
            # Get the first movie from the search results
            movie = data['results'][0]
            movie_id = movie['id']
            
            # Fetch the detailed information about the movie
            movie_response = requests.get(f"{BASE_URL}/movie/{movie_id}", params={
                'api_key': API_KEY
            })
            movie_response.raise_for_status()
            movie_details = movie_response.json()

            # Return the movie details
            return movie_details
        else:
            return "No movie found with that name."

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
