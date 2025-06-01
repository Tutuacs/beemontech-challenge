from redis import StrictRedis
from .models import Log, Schedule
from time import sleep
from .service import update_list

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = StrictRedis(host=host, port=port, db=db)

    def set(self, key, value, ex=None):
        self.redis.set(key, value=str(value), ex=ex)

    def get(self, key):
        return self.redis.get(key)

    def delete(self, key):
        self.redis.delete(key)

    def exists(self, key):
        return self.redis.exists(key)
    
    def Handler(self):
        subscriber = self.redis.pubsub()
        subscriber.subscribe('__keyevent@0__:expired')
        while True:
            message = subscriber.get_message()
            if message:
                channel = message['channel']
                key = message['data']

                if isinstance(channel, bytes):
                    channel = channel.decode('utf-8')
                if isinstance(key, bytes):
                    key = key.decode('utf-8')

                if message['type'] == 'message' and channel == '__keyevent@0__:expired':
                    print(f"Key expired: {key}")
                    Log.objects.create(
                        message=f"Schedule updated with ID {key} starting.",
                        status='START_LIST'
                    )
                    update_list()
                    Log.objects.create(
                        message=f"Schedule updated with ID {key} finished.",
                        status='END_LIST'
                    )
                    Schedule.objects.filter(id=key).update(status='COMPLETED')
            sleep(1)
        