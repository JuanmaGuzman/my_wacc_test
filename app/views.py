# app/views.py
import base64
import hashlib
import hmac
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .utils import (
    get_bitcoin_specific_price,
    get_bitcoin_prices,
    create_chart,
    get_bitcoin_average_price,
)
from .forms import DateSelectionForm, DateRangeSelectionForm

class TypeformSubmission(APIView):
    permission_classes = [AllowAny]

    def verify_signature(self, received_signature, payload):
        WEBHOOK_SECRET = settings.TYPEFORM_CLIENT_SECRET
        print(WEBHOOK_SECRET)
        digest = hmac.new(
            WEBHOOK_SECRET.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256
        ).digest()
        expected_signature = base64.b64encode(digest).decode()

        return received_signature == expected_signature


    def get(self, request, *args, **kwargs):
        # Add your GET method logic here
        return Response({"message": "GET request handled."}, status=status.HTTP_200_OK)


    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = request.data

        received_signature = request.headers.get("typeform-signature")

        if received_signature is None:
            return Response(
                {"Fail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        print(f"received_signature: {received_signature}")
        sha_name, signature = received_signature.split("=", 1)
        if sha_name != "sha256":
            return Response(
                {"Fail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        is_valid = self.verify_signature(signature, request.raw_body)
        if is_valid != True:
            return Response(
                {"Fail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        print(body)

        return Response({}, status=status.HTTP_200_OK)

def index(request):
    bitcoin_prices = get_bitcoin_prices()
    chart = create_chart(bitcoin_prices)

    # Initialize forms
    date_selection_form = DateSelectionForm()
    date_range_form = DateRangeSelectionForm()

    # Handle form submission
    if request.method == 'POST':
        if 'selected_date' in request.POST:
            # Process date selection form
            date_selection_form = DateSelectionForm(request.POST)
            if date_selection_form.is_valid():
                specific_date = date_selection_form.cleaned_data['selected_date']
                specific_value = get_bitcoin_specific_price(specific_date)

                # Update the specific value in the form
                date_selection_form.fields['selected_date'].initial = specific_date

                # Pass data to the context
                context = {
                    "chart": chart,
                    "specific_value": f"Bitcoin value on {specific_date}: {specific_value} USD." if specific_value is not None else f"No data found for {specific_date}.",
                    "date_selection_form": date_selection_form,
                    "date_range_form": date_range_form,
                }
                return render(request, "app/index.html", context)

        elif 'start_date' in request.POST and 'end_date' in request.POST:
            # Process date range form
            date_range_form = DateRangeSelectionForm(request.POST)
            if date_range_form.is_valid():
                start_date = date_range_form.cleaned_data['start_date']
                end_date = date_range_form.cleaned_data['end_date']
                average_price = get_bitcoin_average_price(start_date, end_date)

                # Update the form fields with the submitted values
                date_range_form.fields['start_date'].initial = start_date
                date_range_form.fields['end_date'].initial = end_date

                # Pass data to the context
                context = {
                    "chart": chart,
                    "specific_value": f"Average Bitcoin value between {start_date} and {end_date}: {average_price} USD.",
                    "date_selection_form": date_selection_form,
                    "date_range_form": date_range_form,
                }
                return render(request, "app/index.html", context)

        else:
            # Webhook clause. https://00b7-190-105-177-62.ngrok-free.app
            pass

    # If no form is submitted or forms are not valid, include both forms in the context
    context = {
        "chart": chart,
        "specific_value": "No date selected.",
        "date_selection_form": date_selection_form,
        "date_range_form": date_range_form,
    }

    return render(request, "app/index.html", context)
