import requests
import datetime
import plotly.express as px
from .models import BitcoinPrice

def get_and_save_bitcoin_prices():
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
    data = response.json()

    # Extract historical prices from the API response
    prices = data.get("prices", [])

    # Save prices to the database
    for timestamp, value in prices:
        date_time = datetime.datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')  
        BitcoinPrice.objects.create(date=date_time, value=value)

    return prices

def get_bitcoin_prices():
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
    data = response.json()

    # Extract historical prices from the API response
    prices = data.get("prices", [])

    return prices

def create_chart(prices):
    # Extract timestamps and prices
    timestamps = [timestamp for timestamp, _ in prices]
    prices = [price for _, price in prices]

    # Convert timestamps to human-readable date labels
    date_labels = [datetime.datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d') for timestamp in timestamps]

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
