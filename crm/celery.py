import os
from celery import Celery

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

# Create Celery app
app = Celery("crm")

# Load settings from Django config, namespace = CELERY
app.config_from_object("django.conf:settings", namespace="CELERY")

# Discover tasks inside tasks.py
app.autodiscover_tasks()
