from celery import Celery
from service.main import Manager

cel = Celery('tasks')
cel.config_from_object('celeryconfig')

@cel.task
def add(x, y):
    print('aaa')

@cel.task
def lsi(user_requests):
    Manager(user_requests)
