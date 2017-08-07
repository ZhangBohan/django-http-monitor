import json

from django.http import HttpResponse
from http_monitor import request_monitor

from http_monitor.models import Request
from django.conf import settings


def http_auth(request):
    auth_level = getattr(settings, "HTTP_MONITOR_AUTH_LEVEL", None)
    if auth_level and hasattr(request, 'user') and not getattr(request.user, auth_level):
        return False
    return True


def request_raw(request, request_id):
    if not http_auth(request):
        return HttpResponse("no permit", content_type='text/html')
    content = Request(request_id=request_id).get_conent()
    return HttpResponse(content, content_type='text/html')


@request_monitor
def request_retry(request, request_id):
    if not http_auth(request):
        return HttpResponse("no permit", content_type='text/html')
    r = Request(request_id=request_id).retry(current_request=request)
    return HttpResponse(json.dumps(r), content_type='application/json')


def request(request, request_id):
    if not http_auth(request):
        return HttpResponse("no permit", content_type='text/html')
    result = Request(request_id=request_id).get_request()
    return HttpResponse(json.dumps(result), content_type='application/json')


def requests(request):
    if not http_auth(request):
        return HttpResponse("no permit", content_type='text/html')
    size = int(request.GET.get('size', 20))
    page = int(request.GET.get('page', 1))

    http_requests = Request().get_requests(size=size, page=page)
    return HttpResponse(json.dumps(http_requests), content_type='application/json')
