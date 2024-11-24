import redis
from django.conf import settings

def get_redis_client():
    redis_config = settings.REDIS_CONFIG
    return redis.StrictRedis(
        host=redis_config['HOST'],
        port=redis_config['PORT'],
        db=redis_config['DB'],
        password=redis_config['PASSWORD'],
        ssl=redis_config['SSL']
    )
