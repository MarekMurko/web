from __future__ import absolute_import

import os

import dotenv
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
dotenv.read_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trojsten.settings.production")

app = Celery('trojsten')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
