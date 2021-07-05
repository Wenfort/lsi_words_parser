from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

cel = Celery('tasks')
cel.config_from_object('celeryconfig')
from lsi_words_parser import routes