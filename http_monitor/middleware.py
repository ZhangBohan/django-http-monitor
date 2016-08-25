import uuid

from datetime import datetime
from django.conf import settings

from http_monitor import redis_client


class HttpMonitorMiddleware(object):

    def __init__(self):
        self.expire_seconds = getattr(settings, 'HTTP_MONITOR_EXPIRE_SECONDS', 60 * 60 * 24 * 7)
        self.url_prefix = getattr(settings, 'HTTP_MONITOR_PREFIX', '/api')

    def process_request(self, request):
        request._http_request_body = request.body.decode()

    def process_response(self, request, response):
        path = request.path

        if not settings.DEBUG:
            return response

        if not path.startswith(self.url_prefix):
            return response

        request_id = str(uuid.uuid4())

        pipeline = redis_client.pipeline()
        list_key = 'http_monitor:requests:requests-list'
        pipeline.rpush(list_key, request_id)
        pipeline.ltrim(list_key, 0, 100000)

        item_key_base = 'http_monitor:requests:{requests_id}'.format(requests_id=request_id)
        key = item_key_base + ':request'
        pipeline.hmset(key, {
            'path': path,
            'method': request.method,
            'body': request._http_request_body,
            'host': request.META.get('HTTP_HOST'),
            'status_code': response.status_code,
            'request_id': request_id,
            'created_at': datetime.now().isoformat()
        })
        pipeline.expire(key, self.expire_seconds)

        key = item_key_base + ':request-headers'
        headers = {key: value for key, value in request.META.items() if key.startswith('HTTP_')}
        pipeline.hmset(key, headers)
        pipeline.expire(key, self.expire_seconds)

        key = item_key_base + ':response'
        content = response.content
        pipeline.hmset(key, {
            'status_code': response.status_code,
            'content': content,
            'charset': response.charset,
            'host': request.META.get('HTTP_HOST'),
        })
        pipeline.expire(key, self.expire_seconds)

        key = item_key_base + ':response-headers'
        headers = {key: ', '.join(value) for key, value in response._headers.items()}
        pipeline.hmset(key, headers)
        pipeline.expire(key, self.expire_seconds)

        pipeline.execute()

        response['Request-UUID'] = request_id
        return response
