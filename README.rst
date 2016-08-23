=====
Django http monitor
=====

Django http monitor is a Django middleware for record http request and response in debug

Quick start
-----------

1. Add "http_monitor" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'http_monitor',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^http_monitor/', include('http_monitor.urls')),

3. Add the HttpMonitorMiddleware for monitor request like this::

    MIDDLEWARE_CLASSES = (
        'apps.http_monitor.middleware.HttpMonitorMiddleware',
        ...
    )

    Note HttpMonitorMiddleware should be in top of the middlewares,
    But GZipMiddleware will zip the content, so GZipMiddleware will be top.


4. Start the development server and visit http://127.0.0.1:8000/http_monitor/requests
   (you'll need the Admin login status to see this)
