from celery import Celery
from src.config import settings

celery_instance = Celery(
    "tasks",
    borker=settings.redis_url,
    include=[
        "src.tasks.tasks",
    ],
)

# celery_instance.conf.beat_schedule = {
#     "luboe-nazvanie": {
#         "task": "booking_today_checkin",
#         "schedule": 5,
#     }
# }
