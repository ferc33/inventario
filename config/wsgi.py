import os
from django.core.wsgi import get_wsgi_application

# Point to your Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.production')

application = get_wsgi_application()
