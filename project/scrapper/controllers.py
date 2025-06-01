import json
from .service import list, update_list
from .models import Quote, Log
from django.http import HttpResponse
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