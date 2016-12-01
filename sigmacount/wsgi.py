"""
WSGI config for sigmacount project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os,sys,site

from django.core.wsgi import get_wsgi_application


sys.path.append('/home/teddy/Development/django/')
sys.path.append('/home/teddy/Development/django/sigmacount/')
sys.path.append('/home/teddy/Development/django/sigmacount/sigmacount/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sigmacount.settings")

application = get_wsgi_application()
