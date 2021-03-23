from celery import shared_task
from .notino import get_notino_urls, save_urls_watched_to_json, get_notino_fragrance_data_and_update_fragrances_db, send_email_with_fragrances
from .models import URL, Fragrance
import json
import os
import time
from django.conf import settings
from django.core import serializers
from celery.schedules import crontab
from notino_watcher.celery import app

@shared_task(name='fragrance_get_notino_fragrances_task')
def get_notino_fragrances_task():
    for url in get_notino_urls():
        get_notino_fragrance_data_and_update_fragrances_db_task.delay(url)

@shared_task(name='fragrance_get_notino_fragrance_data_and_update_fragrances_db_task')
def get_notino_fragrance_data_and_update_fragrances_db_task(url):
    get_notino_fragrance_data_and_update_fragrances_db(url)

@shared_task(name='fragrance_save_urls_watched_to_json_task')
def save_urls_watched_to_json_task():
    file_path = 'fragrance/static/fragrance/urls_watched.json'
    save_urls_watched_to_json(file_path)

@shared_task(name='fragrance_send_email_with_fragrances_task')
def send_email_with_fragrances_task(fragrances, addressee):
    send_email_with_fragrances(fragrances, addressee)

@shared_task(name='fragrance_look_notino_fragrances_task')
def look_notino_fragrances_task():
    get_notino_fragrances_task.delay()
    time.sleep(10)
    cheap_offers = Fragrance.objects.cheap_offers()
    fragrances_data = serializers.serialize('json', cheap_offers)
    fragrances_data = [fragrance['fields'] for fragrance in json.loads(fragrances_data)]
    send_email_with_fragrances_task.delay(fragrances_data, settings.ADDRESSEE)

@shared_task(name='demo_task')
def demo_task(x):
    print('Demo')
    print(x)

@shared_task(name='demo2_task')
def demo2_task():
    print('Demo2')
    demo_task.delay('hola demo')