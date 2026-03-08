import os
from django.core.wsgi import get_wsgi_application

# Ensure this matches your project folder name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hangarin_project.settings')

application = get_wsgi_application()