from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from scrapper.models import Log, Quote, Schedule
from scrapper.serializers import LogSerializer, QuoteSerializer, ScheduleSerializer
from .redis_client import RedisClient
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

class QuoteViewSet(ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

class LogViewSet(ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    
class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        try:
            redis_client = RedisClient()
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            # If Redis connection fails, delete the created schedule
            schedule_id = response.data.get('id')
            if schedule_id:
                Schedule.objects.filter(id=schedule_id).delete()
            response.data = {'error': 'Failed to connect to Redis, schedule not created.'}
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        try:
            schedule_id = response.data['id']
            instance = Schedule.objects.get(id=schedule_id)

            expiration_date = instance.date - timezone.now()
            expiration_seconds = int(expiration_date.total_seconds())

            if expiration_seconds > 0:
                redis_client.set(instance.id, instance.id, ex=expiration_seconds)
            else:
                instance.status = 'FAILED'
                instance.name = instance.name + ' - Failed to set Redis key'
                instance.save()
                response.data['status'] = instance.status
                response.data['name'] = instance.name

        except Exception as e:
            print(f"Error processing Redis logic: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response

    def list(self, request, *args, **kwargs):
        toUpdate = self.queryset.filter(status='PENDING', date__lte=datetime.now())
        if toUpdate.exists():
            toUpdate.update(status='FAILED')
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance and instance.status == 'PENDING' and instance.date <= datetime.now():
            instance.status = 'FAILED'
            instance.save()
        return super().retrieve(request, *args, **kwargs)