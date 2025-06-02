import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes.settings')
django.setup()

from django.core.management.base import BaseCommand
from scrapper.redis_client import RedisClient

class Command(BaseCommand):
    help = 'Subscribe to Redis channels and process messages'

    def handle(self, *args, **kwargs):
        client = RedisClient()
        client.Handler()
