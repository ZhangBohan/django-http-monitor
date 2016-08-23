import redis
from django.conf import settings

try:
    url = settings.HTTP_MONITOR_REDIS_URL
except AttributeError:
    url = 'redis://localhost:6379/0'

redis_client = redis.StrictRedis.from_url(url, decode_responses=True)
