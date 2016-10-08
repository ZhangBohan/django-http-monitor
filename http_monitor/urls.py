from django.conf.urls import url
from http_monitor import views


urlpatterns = [
    url(r'^requests/$', views.requests, name='django.http_monitor.requests'),
    url(r'^requests/(?P<request_id>.*)/raw/$', views.request_raw, name='django.http_monitor.request_raw'),
    url(r'^requests/(?P<request_id>.*)/retry/$', views.request_retry, name='django.http_monitor.request_retry'),
    url(r'^requests/(?P<request_id>.*)/$', views.request, name='django.http_monitor.request'),
]
