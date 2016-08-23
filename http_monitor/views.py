import json
from functools import wraps

from django.http import JsonResponse, HttpResponseForbidden

from http_monitor import redis_client


def staff_only(api_func):
    @wraps(api_func)
    def _warp(request, *args, **kwargs):
        if not request.user.id or not request.user.is_staff:
            return HttpResponseForbidden()
        return api_func(request, *args, **kwargs)
    return _warp


@staff_only
def request(request, request_id):
    item_key_base = 'http_monitor:requests:{requests_id}'.format(requests_id=request_id)

    pipeline = redis_client.pipeline()
    key = item_key_base + ':request'
    pipeline.hgetall(key)

    key = item_key_base + ':request-headers'
    pipeline.hgetall(key)

    key = item_key_base + ':response'
    pipeline.hgetall(key)

    key = item_key_base + ':response-headers'
    pipeline.hgetall(key)

    http_request, request_headers, response, response_headers = pipeline.execute()
    try:
        content = response.get('content')
        content = json.loads(content)
    except Exception:
        content = 'http monitor decode error!!!!! this is not raw response, but json can not show this'

    response['content'] = content

    result = {
        'request': http_request,
        'request_headers': request_headers,
        'response': response,
        'response_headers': response_headers
    }
    return JsonResponse(result)


@staff_only
def requests(request):
    size = int(request.GET.get('size', 20))
    page = int(request.GET.get('page', 1))
    request_ids = redis_client.lrange('http_monitor:requests:requests-list', -size * page, - ((page - 1) * size + 1))
    request_ids.reverse()
    pipeline = redis_client.pipeline()

    for request_id in request_ids:
        item_key_base = 'http_monitor:requests:{requests_id}'.format(requests_id=request_id)
        key = item_key_base + ':request'
        pipeline.hgetall(key)

    http_requests = pipeline.execute()
    return JsonResponse(http_requests, safe=False)
