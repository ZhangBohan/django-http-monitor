# Django http monitor

Django http monitor is a Django middleware for record http request and response in debug

Quick start
-----------

## Install

```
pip install django-http-monitor
```

## Install apps

Add "http_monitor" to your INSTALLED_APPS setting like this::

```
INSTALLED_APPS = [
    ...
    'http_monitor',
]
```

## Include url

Include the http monitor URLconf in your project urls.py like this::

```
url(r'^http_monitor/', include('http_monitor.urls')),
```

##  Add middleware
Add the HttpMonitorMiddleware for monitor request like this::

```
MIDDLEWARE_CLASSES = (
    'apps.http_monitor.middleware.HttpMonitorMiddleware',
    ...
)
```

Note HttpMonitorMiddleware should be in top of the middlewares,
But GZipMiddleware will zip the content, so GZipMiddleware will be top.


## Done

Start the development server and visit http://127.0.0.1:8000/http_monitor/requests
   (you'll need the Admin login status to see this)
