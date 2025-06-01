from django.urls import path
from rest_framework import routers
from .controllers import live_list, update_list, pandas_json_df, pandas_csv_df
from .view_sets import QuoteViewSet, LogViewSet, ScheduleViewSet

router = routers.DefaultRouter()
router.register('quote', QuoteViewSet, basename='Quote')
router.register('logs', LogViewSet, basename='Log')
router.register('schedule', ScheduleViewSet, basename='Schedule')

urlpatterns = [
    path('live', live_list, name='live_scrapper'),
    path('update', update_list, name='update_scrapper'),
    path('pandas/json', pandas_json_df, name='pandas_json_df'),
    path('pandas/csv', pandas_csv_df, name='pandas_csv_df'),
] + router.get_urls()