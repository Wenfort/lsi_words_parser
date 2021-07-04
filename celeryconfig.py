broker_url = 'redis://localhost:6379/0'
result_backend = 'rpc://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True

task_annotations = {
    'tasks.add': {'rate_limit': '1/m'}
}