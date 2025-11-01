from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

from src.database import Database
from src.config import settings


app = Celery(
    "gradewise",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL,
    include=["src.grade.tasks"],  
)

# Celery configuration
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,  # Important for Flower to show tasks
    task_time_limit=300,  # 5 minutes hard limit
    task_soft_time_limit=270,  # 4.5 minutes soft limit
    worker_prefetch_multiplier=1,  # Process one task at a time (good for long tasks)
    worker_max_tasks_per_child=50,  # Restart worker after 50 tasks (prevent memory leaks)
)

@worker_process_init.connect
def setup_celery_worker(**kwargs):
    print("Initializing database connection for Celery worker...")
    try:
        Database.create_sync_session()
        print("Database initialized successfully in worker.")
    except Exception as e:
        print(f"Error initializing database in worker: {e}")


@worker_process_shutdown.connect
def shutdown_celery_worker(**kwargs):
    """Clean up when worker shuts down"""
    try:
        Database.close_sync()
        print("Database closed successfully in worker.")
    except Exception as e:
        print(f"Error closing database in worker: {e}")