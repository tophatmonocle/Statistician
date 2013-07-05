import sys
import os
APP_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(APP_DIR)

from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

