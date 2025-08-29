#!/bin/bash

PROJECT_PATH="/var/www/crm"
PYTHON_ENV_PATH="$PROJECT_PATH/venv/bin/activate"
MANAGE_PY_PATH="$PROJECT_PATH/manage.py"

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
PYTHON_CODE="import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings'); import django; django.setup(); from crm_app.models import Customer; from django.utils import timezone; from datetime import timedelta; threshold_date = timezone.now() - timedelta(days=365); inactive_customers = Customer.objects.filter(last_active__lt=threshold_date); count = inactive_customers.count(); inactive_customers.delete(); print(f'Deleted {count} inactive customers.');"