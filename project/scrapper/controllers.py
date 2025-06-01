import json
from .service import list
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
    quotes = list(log=True)
    if quotes:
        created_quotes = 0
        for quote in quotes:

            exist = Quote.objects.filter(text=quote['text'], author=quote['author']).first()
            if exist:
                continue

            created_quote = Quote.objects.create(
                text=quote['text'],
                author=quote['author'],
                tags=quote['tags'],
                page=quote['page']
            )

            if not created_quote:
                Log.objects.create(
                    message=f"Error creating quote: {quote['text']}",
                    status='ERROR_CREATING'
                )
                continue
            created_quotes += 1
        return HttpResponse("List updated successfully. {} new quotes created.".format(created_quotes))

    return HttpResponse("Update list functionality is not implemented yet.")

@swagger_auto_schema(
    method='get',
    operation_description="Schedule a task to update the list of quotes"
)
@api_view(['GET'])
def schedule_update(request):
    # This function is a placeholder for scheduling tasks.
    # In a real application, you would use a task queue like Celery.
    return HttpResponse("Scheduling update task is not implemented yet.")