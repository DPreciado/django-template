"""
WSGI config for djangoproject project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys

from pathlib import Path
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Esto nomas lo cambia Claudio desde el servidor de produccion.
BASE_DIR = Path(__file__).resolve().parent.parent
# sys.path.append(BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')

application = get_wsgi_application()