import os, sys

sys.stdout = sys.stderr

ALLDIRS = ['/projects/readthedocs/lib/python2.6/site-packages']
import site 

# Remember original sys.path.
prev_sys_path = list(sys.path) 

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path 


sys.path.append('/projects/readthedocs/checkouts/readthedocs.org/readthedocs')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.postgres'
os.environ['CELERY_LOADER'] = 'django'

activate_this = "/projects/readthedocs/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
