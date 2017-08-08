import json

from django.http import HttpResponse
from http_monitor import request_monitor, auth_permission

from http_monitor.models import Request
from django.conf import settings


@auth_permission
def request_raw(request, request_id):
    content = Request(request_id=request_id).get_conent()
    return HttpResponse(content, content_type='text/html')

@auth_permission
@request_monitor
def request_retry(request, request_id):
    r = Request(request_id=request_id).retry(current_request=request)
    return HttpResponse(json.dumps(r), content_type='application/json')


@auth_permission
def request(request, request_id):
    result = Request(request_id=request_id).get_request()
    return HttpResponse(json.dumps(result), content_type='application/json')


@auth_permission
def requests(request):
    size = int(request.GET.get('size', 20))
    page = int(request.GET.get('page', 1))

    http_requests = Request().get_requests(size=size, page=page)
    return HttpResponse(json.dumps(http_requests), content_type='application/json')
