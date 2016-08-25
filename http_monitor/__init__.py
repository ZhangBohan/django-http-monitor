import redis
from django.conf import settings


url = getattr(settings, 'HTTP_MONITOR_REDIS_URL', 'redis://localhost:6379/0')
url_prefix_list = getattr(settings, 'HTTP_MONITOR_PREFIX_LIST', ['/'])
exclude_url_prefix_list = getattr(settings, 'HTTP_MONITOR_EXCLUDE_URL_PREFIX_LIST', ['/http_monitor'])
expire_seconds = getattr(settings, 'HTTP_MONITOR_EXPIRE_SECONDS', 60 * 60 * 24 * 7)

store_prefix = getattr(settings, 'HTTP_MONITOR_STORE_PREFIX', 'http_monitor:')

redis_client = redis.StrictRedis.from_url(url, decode_responses=True)
