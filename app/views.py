from django.shortcuts import render
from .utils import get_bitcoin_specific_price, get_bitcoin_prices, create_chart
from .forms import DateSelectionForm  # Import your form

def index(request):
    bitcoin_prices = get_bitcoin_prices()
    chart = create_chart(bitcoin_prices)

    # Handle form submission
    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            specific_date = form.cleaned_data['selected_date']
            specific_value = get_bitcoin_specific_price(specific_date)

            # Pass data to the context
            context = {
                "chart": chart,
                "specific_value": f"Bitcoin value on {specific_date}: {specific_value}" if specific_value is not None else f"No data found for {specific_date}.",
                "form": form,  # Include the form in the context for redisplaying it in case of errors
            }
            return render(request, "app/index.html", context)

    # If the form is not submitted or is invalid, initialize the form
    else:
        form = DateSelectionForm()

    # Pass data to the context
    context = {
        "chart": chart,
        "specific_value": None,  # Initial value
        "form": form,
    }

    return render(request, "app/index.html", context)
