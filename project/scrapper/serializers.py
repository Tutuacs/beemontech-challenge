from rest_framework import serializers
from .models import Quote, Log

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'