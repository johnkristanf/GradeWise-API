from celery import Celery
from celery.signals import worker_process_init

from src.database import Database
from src.config import settings

# Assuming these are defined and available


# --- 1. CELERY CONFIGURATION CLASS ---
class CeleryConfig:
    """Standard configuration for Celery."""

    broker_url = settings.CELERY_BROKER_URL
    result_backend = settings.CELERY_BACKEND_URL
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    timezone = "UTC"
    enable_utc = True
    task_track_started = True
    task_time_limit = 300
    task_soft_time_limit = 270


celery_app = Celery("gradewise")
celery_app.config_from_object(CeleryConfig)
celery_app.autodiscover_tasks(["src.tasks"])


@worker_process_init.connect
def setup_celery_worker(**kwargs):
    print("Initializing database connection for Celery worker...")
    try:
        Database.initialize()
        print("Database initialized successfully in worker.")
    except Exception as e:
        print(f"Error initializing database in worker: {e}")
