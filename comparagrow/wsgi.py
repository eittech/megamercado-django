import os
import sys

path='/home/omar/comparagrow'

if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'comparagrow.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
