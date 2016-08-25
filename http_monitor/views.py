import json

from django.http import HttpResponse

from http_monitor import redis_client, store_prefix


def request_raw(request, request_id):
    item_key_base = store_prefix + 'requests:{requests_id}'.format(requests_id=request_id)
    key = item_key_base + ':response'
    content = redis_client.hget(key, 'content')
    return HttpResponse(content, content_type='text/html')


def request(request, request_id):
    item_key_base = store_prefix + 'requests:{requests_id}'.format(requests_id=request_id)

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
    if not http_request:
        return HttpResponse(status=404)

    try:
        content = response.get('content')
        content = json.loads(content)
    except Exception:
        content = 'HTTP monitor json decode error.'

    response['content'] = content

    result = {
        'request': http_request,
        'request_headers': request_headers,
        'response': response,
        'response_headers': response_headers
    }
    return HttpResponse(json.dumps(result), content_type='application/json')


def requests(request):
    size = int(request.GET.get('size', 20))
    page = int(request.GET.get('page', 1))
    request_ids = redis_client.lrange(store_prefix + 'requests:requests-list', -size * page, - ((page - 1) * size + 1))
    request_ids.reverse()
    pipeline = redis_client.pipeline()

    for request_id in request_ids:
        item_key_base = store_prefix + 'requests:{requests_id}'.format(requests_id=request_id)
        key = item_key_base + ':request'
        pipeline.hgetall(key)

    http_requests = pipeline.execute()
    return HttpResponse(json.dumps(http_requests), content_type='application/json')
