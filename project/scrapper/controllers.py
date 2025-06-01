import json
import csv
import pandas as pd
from .models import Quote, Log
from django.http import HttpResponse
from .service import list, update_list
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve live list of quotes"
)
@api_view(['GET'])
def live_list(request):
    quotes = list()

    if quotes:
        quotes_json = json.dumps({"list": quotes})
        return HttpResponse(quotes_json, content_type="application/json")
    return HttpResponse("Live list of quotes will be displayed here.")

@swagger_auto_schema(
    method='get',
    operation_description="Update the list of quotes from a source and create new entries if they do not exist"
)
@api_view(['GET'])
def update_list(request):
    created_quotes = update_list(True)
    return HttpResponse("List updated successfully. {} new quotes created.".format(created_quotes))

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve quotes as a Pandas DataFrame in JSON format"
)
@api_view(['GET'])
def pandas_json_df(request):
    quotes = Quote.objects.all().values()
    df = pd.DataFrame(quotes)
    df_json = df.to_json(orient='records')
    return HttpResponse(df_json, content_type="application/json")

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve quotes as a Pandas DataFrame in CSV format"
)
@api_view(['GET'])
def pandas_csv_df(request):
    quotes = Quote.objects.all().values()
    df = pd.DataFrame(quotes)

    # Prepare the HTTP response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="quotes.csv"'

    # Write DataFrame to CSV with safe quoting
    df.to_csv(
        path_or_buf=response,
        index=False,
        quotechar='"',
        quoting=csv.QUOTE_ALL,
        encoding='utf-8-sig'  # Optional for Excel compatibility
    )
    return response