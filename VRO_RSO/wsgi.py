"""
WSGI config for VRO_RSO project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

try:
    sys.path.remove('/usr/lib/python3/dist-packages')
except:
    pass

sys.path.append('/root/public_html/')
sys.path.append('/root/env/lib/python3.10/site-packages/')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VRO_RSO.settings')

application = get_wsgi_application()

