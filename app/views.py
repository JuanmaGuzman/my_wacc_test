from django.shortcuts import render
from .models import BitcoinPrice
from .utils import get_and_save_bitcoin_prices, get_bitcoin_prices, create_chart

def index(request):
    # Check if the BitcoinPrice table is empty
    # if BitcoinPrice.objects.exists():
    #     # Fetch data from the database
    #     bitcoin_prices = BitcoinPrice.objects.all().values_list('date', 'value')
    # else:
    #     # If the table is empty, fetch data from the API and save to the database
    #     get_and_save_bitcoin_prices()
    #     bitcoin_prices = BitcoinPrice.objects.all().values_list('date', 'value')

    bitcoin_prices = get_bitcoin_prices()
    chart = create_chart(bitcoin_prices)

    # Pass data to the context
    context = {
        "chart": chart,
    }

    return render(request, "app/index.html", context)
