# scrapper/management/commands/subscribe.py
from django.core.management.base import BaseCommand
from ...redis_client import RedisClient

class Command(BaseCommand):
    help = 'Subscribe to Redis channels and process messages'

    def handle(self, *args, **kwargs):
        client = RedisClient()
        client.Handler()
