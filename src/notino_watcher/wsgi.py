"""
WSGI config for notino_watcher project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/


You can run the app with gunicorn

gunicorn notino_watcher.wsgi --bind 0.0.0.0:8000

Remember to do before:
    -/manage.py collectstatic
    DEBUG=False
"""


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notino_watcher.settings')

application = get_wsgi_application()
