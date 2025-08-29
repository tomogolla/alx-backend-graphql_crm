# CRM Celery Setup

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

### 2 Install and start redis

sudo apt-get install redis-server
redis-server

### 3. Run migrations

sudo apt-get install redis-server
redis-server

### 4. start celery worker

celery -A crm worker -l info

### 5. Start celery beat schedular

celery -A crm worker -l info

### 6. Verify logs

cat /tmp/crm_report_log.txt
