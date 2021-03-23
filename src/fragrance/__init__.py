#from .tasks import get_notino_fragrance_data_and_update_fragrances_db_task
from celery import current_app

#get_notino_fragrance_data_and_update_fragrances_db_task.delay()

current_app.send_task(
    'fragrance_get_notino_fragrances_task',
    queue='default',
    ignore_result=True,
)