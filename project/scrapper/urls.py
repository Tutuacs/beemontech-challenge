from django.urls import path
from rest_framework import routers
from .controllers import live_list, update_list
from .view_sets import QuoteViewSet, LogViewSet, ScheduleViewSet

router = routers.DefaultRouter()
router.register('quote', QuoteViewSet, basename='Quote')
router.register('logs', LogViewSet, basename='Log')
router.register('schedule', ScheduleViewSet, basename='Schedule')

urlpatterns = [
    path('live', live_list, name='live_scrapper'),
    path('update', update_list, name='update_scrapper'),
] + router.get_urls()