from rest_framework.viewsets import ModelViewSet
from scrapper.models import Log, Quote
from scrapper.serializers import LogSerializer, QuoteSerializer

class QuoteViewSet(ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

class LogViewSet(ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    
    