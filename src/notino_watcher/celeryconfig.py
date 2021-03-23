"""
broker_url = "redis://localhost:6380"
result_backend = 'redis://localhost:6380'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['application/json']
timezone = 'Europe/Madrid'
enable_utc = True
"""


task_routes = {
    'demo_some_demo_task': 'low-priority',
}
task_annotations = {
    'demo_some_demo_task': {'rate_limit': '1/m'},
}
