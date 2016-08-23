from django.conf.urls import url
from http_monitor import views


urlpatterns = [
    url(r'^requests/?$', views.requests, name='django.http_monitor.requests'),
    url(r'^requests/(?P<request_id>.*)/?$', views.request, name='django.http_monitor.request'),
]
