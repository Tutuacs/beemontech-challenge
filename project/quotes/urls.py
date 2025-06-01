from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Quotes to Scrape",
      default_version='v1',
      description="API que retorna quotes e logs do banco de dados do site principal que faz um trabalho de raspagem do site 'quotes.toscrape.com'",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# router = routers.DefaultRouter()
# router.register('scrapper', LogListAPI, basename='logAPI')
# router.register('quoteAPI', QuoteListAPI, basename='quoteAPI')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrapper/', include('scrapper.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
]
