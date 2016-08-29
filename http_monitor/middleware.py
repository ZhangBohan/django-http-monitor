from django.conf import settings

from http_monitor import url_prefix_list, exclude_url_prefix_list
from http_monitor.models import Request


class HttpMonitorMiddleware(object):

    def process_request(self, request):
        request._http_request_body = request.body.decode()

    def process_response(self, request, response):
        path = request.path

        if not settings.DEBUG:
            return response

        if not hasattr(response, 'content'):
            return response

        for url_prefix in url_prefix_list:
            if not path.startswith(url_prefix):
                return response

        for url_prefix in exclude_url_prefix_list:
            if path.startswith(url_prefix):
                return response

        response['Request-UUID'] = Request().add_request(request=request, response=response)
        return response
