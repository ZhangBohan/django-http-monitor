# Django http monitor

Django http monitor is a Django app for record http request and response in debug.

Django http monitor is based on response header `Request-UUID`, anyone has any questions about the request, just send me `Request-UUID` in response header, we can see whole message what we what.

## Quick start

### Install

```
pip install django-http-monitor
```

### Install apps

Add "http_monitor" to your INSTALLED_APPS setting like this::

```
INSTALLED_APPS = [
    ...
    'http_monitor',
]
```

### Include url

Include the http monitor URLconf in your project urls.py like this::

```
url(r'^http_monitor/', include('http_monitor.urls')),
```

### Add middleware
Add the HttpMonitorMiddleware for monitor request like this::

```
MIDDLEWARE_CLASSES = (
    'http_monitor.middleware.HttpMonitorMiddleware',
    ...
)
```

Note HttpMonitorMiddleware should be in top of the middlewares,
But GZipMiddleware will zip the content, so GZipMiddleware will be top.


### Done

Start the development server and visit http://127.0.0.1:8000/http_monitor/requests


## Settings

### HTTP_MONITOR_REDIS_URL
A redis url for store debug message

### HTTP_MONITOR_FORCE_URL_LIST
a list for which prefix match list will be force record.

### HTTP_MONITOR_PREFIX_LIST
A list for which prefix start will be monitor, default is `['/']`

### HTTP_MONITOR_EXCLUDE_URL_PREFIX_LIST
A list for which prefix start will **not** be monitor, default is `['/http_monitor']`

### HTTP_MONITOR_EXPIRE_SECONDS
How long will redis expire the monitoring request, default is one week

## URLs

Current we have three urls provide

- `^requests/` monitoring request list
- `^requests/(?P<request_id>.*)/` monitoring request item
- `^requests/(?P<request_id>.*)/raw/` monitoring request item response content（for content can't decode to json）
- `^requests/(?P<request_id>.*)/retry/` retry request

## Develop

```
rm dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
```
