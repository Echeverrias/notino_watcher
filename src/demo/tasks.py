from notino_watcher.celery import app
from celery import shared_task
from demo.demo import some_demo
from celery.decorators import task
from celery.schedules import crontab
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task(bind=True)
def debug_task(self, name="debug_task"): #default name: 'demo.tasks.debug_task'
    print(f'Request: {self.request}')

@task(name='demo_some_demo_task')
def some_demo_task(x):
    x = x or 'SOME_TASK'
    return some_demo(x)


@shared_task(name='demo_some_demo_shared_task')
def some_demo_shared_task(x):
    x = x or 'SOME_SHARED_TASK'
    return some_demo(x)


@app.on_after_configure.connect # No funciona
def setup_periodic_tasks(sender, **kwargs):
    pass
    # Calls test('hello') every 10 seconds.
   # sender.add_periodic_task(10.0, some_demo_task.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
   # sender.add_periodic_task(30.0, some_demo_task.s('world'), expires=10, name='expires 10')

    # Executes every Monday morning at 7:30 a.m.
    """
    sender.add_periodic_task(
        crontab(hour=23, minute=30, day_of_week=3),
        some_demo_task.s('Happy Wednesday!'),
    )
    """


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    # Calls test('hello') every 10 seconds.
    #sender.add_periodic_task(10.0, some_demo_task.s('hello finalize'), name='periodic_some_demo_task')
   # sender.add_periodic_task(10.0, debug_task.s())

    #sender.add_periodic_task(5.0, some_demo_task.s('some_demo_task.s'), expires=10, name='some_demo_task.s')
    #sender.add_periodic_task(5.0, some_demo_task.delay('some_demo_task.delay'), expires=10, name='some_demo_task.delay')
    # Calls test('world') every 30 seconds
    #sender.add_periodic_task(30.0, some_demo_task.s('world finalize'), expires=10, name='expires 10 finalize')

    # Executes every Monday morning at 7:30 a.m.
    """
    sender.add_periodic_task(
        crontab(hour=23, minute=30, day_of_week=3),
        some_demo_task.s('Happy Wednesday finalize!'),
    )
    """
    pass


from celery import current_app

current_app.send_task(

    "demo_some_demo_task",

    args=("send_task",),

    queue="default",

    ignore_result=True )




