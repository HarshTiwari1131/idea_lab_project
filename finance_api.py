import requests

# Alpha Vantage API configuration
api_key = "2CITJVD5WLHI2LFM"
base_url = "https://www.alphavantage.co/query"

def get_stock_data(symbol, interval="1min"):
    """Fetch intraday stock data from Alpha Vantage API and return the latest stock data."""
    # Parameters for the API request
    params = {
        "function": "TIME_SERIES_INTRADAY",  # Intraday time series
        "symbol": symbol,                    # Stock symbol (e.g., "AAPL" for Apple)
        "interval": interval,                # Interval between data points (e.g., "1min", "5min", "15min", etc.)
        "apikey": api_key                    # Your API key
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check for a successful response
    if response.status_code == 200:
        data = response.json()
        # Dynamically access the time series key based on the interval
        key = f"Time Series ({interval})"
        if key in data:
            # Get the latest available time and stock info
            latest_time = list(data[key].keys())[0]
            latest_data = data[key][latest_time]

            # Create a summary of stock data for the latest time
            stock_summary = (f"Stock data for {symbol.upper()} at {latest_time}: "
                             f"Open: {latest_data['1. open']}, "
                             f"High: {latest_data['2. high']}, "
                             f"Low: {latest_data['3. low']}, "
                             f"Close: {latest_data['4. close']}, "
                             f"Volume: {latest_data['5. volume']}")
            
            return stock_summary
        else:
            return f"Error: {data.get('Note', 'No data available or API limit reached.')}"
    else:
        return "Failed to retrieve data. Please check the symbol and API key."

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     print(get_stock_data("AAPL"))
