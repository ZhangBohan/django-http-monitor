import time

from django.conf import settings

from http_monitor import url_prefix_list, exclude_url_prefix_list, force_url_list
from http_monitor.models import Request


class HttpMonitorMiddleware(object):

    def process_request(self, request):
        try:
            request._http_request_body = request.body.decode()
            request._start_time = time.time()
        except Exception:
            pass

    def process_response(self, request, response):
        if not hasattr(request, '_http_request_body'):
            return response

        path = request.path

        if path not in force_url_list:

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

        if hasattr(request, '_start_time'):
            performance = time.time() - request._start_time
            response['API-performance'] = performance
            request._start_time = None
        response['Request-UUID'] = Request().add_request(request=request, response=response)
        return response
