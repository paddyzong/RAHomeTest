import redis
from django.conf import settings

redis_config = settings.REDIS_CONFIG
connection_pool = redis.ConnectionPool(
    host=redis_config['HOST'],
    port=redis_config['PORT'],
    db=redis_config['DB'],
    password=redis_config['PASSWORD'],
    #ssl=redis_config['SSL']
)

def get_redis_client():
    # Use the connection pool to create a Redis client
    return redis.StrictRedis(connection_pool=connection_pool)
