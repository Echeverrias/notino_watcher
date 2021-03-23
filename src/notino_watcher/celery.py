from __future__ import absolute_import  # , unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notino_watcher.settings')

app = Celery('notino_watcher')  # Se le asigna el nombre del modulo/carpeta contenedora

# app = Celery('djangoapp', broker="redis://localhost:6379") # Se le asigna el broker

# app = Celery('djangoapp', backend="redis://localhost:6379" broker="redis://localhost:6379")Se puede especificar aquí también el backend y el backend_result

# Using a string here means the worker will not have to
# pickle the object when using Windows.

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix. (Constantes declaradas ej: CELERY_BROKER_URL = "redis://localhost:6379")

# Indica que las variables de configuración están en settings.py con el prefijo CELERY (podrían estar en otro módulo)
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.config_from_object('djangoapp.celeryconfig')
# Busca los ficheros llamados tasks para registrar las tareas
# Load task modules from all registered Django app configs.
# This tells Celery to try to automatically discover a file called tasks.py in all of our Django apps

app.autodiscover_tasks() # Busca por defecto en las apps

#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
