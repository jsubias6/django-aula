import os
import sys

sys.path.append('/opt/django-aula')

os.environ['DJANGO_SETTINGS_MODULE'] = 'aula.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
