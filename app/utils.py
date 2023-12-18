import requests
import datetime as dt
from datetime import datetime, timedelta
import plotly.express as px
from .models import BitcoinValue

def get_bitcoin_prices():
    try:
        # CoinGecko API endpoint for historical prices
        api_url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        
        # Parameters for the API request (you can customize the time range as needed)
        params = {
            "vs_currency": "usd",
            "days": 5500,
            "interval": "daily",
        }

        # Make the API request
        response = requests.get(api_url, params=params)

        # Raise an exception for non-200 status codes
        response.raise_for_status()

        data = response.json()

        # Extract historical prices from the API response
        prices = data.get("prices", [])

        return prices
    except requests.exceptions.RequestException as e:
        # Handle API request failure (e.g., log the error, raise an exception, etc.)
        print(f"Failed to fetch Bitcoin prices from Coingecko API. Error: {e}")
        return None


def create_chart(prices):
    try:
        # Check if prices is not None and is iterable
        if prices is None or not hasattr(prices, '__iter__'):
            raise ValueError("Invalid prices data. Prices should be a non-null iterable.")

        # Extract timestamps and prices
        timestamps = [timestamp for timestamp, _ in prices]
        prices = [price for _, price in prices]

        # Check if timestamps and prices are not None and are iterable
        if timestamps is None or prices is None or not hasattr(timestamps, '__iter__') or not hasattr(prices, '__iter__'):
            raise ValueError("Invalid timestamps or prices data. Both should be non-null iterables.")

        # Convert timestamps to human-readable date labels
        date_labels = [dt.datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d') for timestamp in timestamps]

        # Create a Plotly line chart
        fig = px.area(x=date_labels,
                      y=prices,
                      labels={"x": "Choose specific date range", "y": "Price (USD)"},
                      title="Bitcoin Historical Prices",
                      color_discrete_sequence=['#f7931a'],  # Set the line color
                      )

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        # Convert the chart to JSON to pass to the template
        chart_json = fig.to_json()

        return chart_json
    except Exception as e:
        # Handle any exceptions that might occur during chart creation
        print(f"Error creating chart: {e}")
        return None


def get_bitcoin_specific_price(specific_date):
    formatted_date_str = specific_date.strftime("%d-%m-%Y")

    # Check if the value for the specific date exists in the database
    try:
        existing_value = BitcoinValue.objects.get(date=specific_date)
        print("¡¡Date existed on the Database!!")
        return existing_value.value
    except BitcoinValue.DoesNotExist:
        print("¡¡Date does not existed on the Database!! Let's search for it using the API.")
        # If the value doesn't exist, fetch it from Coingecko API
        api_url = "https://api.coingecko.com/api/v3/coins/bitcoin/history"

        params = {
            "date": formatted_date_str,
        }

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()

            if response.status_code == 200:
                price = int(data["market_data"]["current_price"]["usd"])

                # Save the retrieved value to the database
                new_value = BitcoinValue(date=specific_date, value=price)
                new_value.save()

                print(f"PRICE: {price}")

                return price
            else:
                print(f"Failed to fetch data from Coingecko API. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            return None


def get_bitcoin_average_price(start_date, end_date):
    total = 0
    avg = 0

    # Convert datetime.date to datetime.datetime with time set to midnight
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)  # Add one day to include the end date

    api_url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"

    params = {
        "vs_currency": "usd",
        "from": int(start_datetime.timestamp()),
        "to": int(end_datetime.timestamp()),
    }

    response = requests.get(api_url, params=params)
    
    try:
        response.raise_for_status()
        data = response.json()

        if response.status_code == 200:
            prices = data.get("prices", [])

            if prices:
                for item in prices:
                    total += item[1]

                avg = total / len(prices)

        return avg

    except requests.exceptions.RequestException as e:
        print(f"Error in API request: {e}")

        return "To many requests"
