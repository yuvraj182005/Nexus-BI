from celery import Celery

from app.core.config import get_settings

settings = get_settings()
celery_app = Celery("nexusbi", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.include = ["app.tasks.dataset", "app.tasks.connector"]
celery_app.conf.update(
	task_serializer="json",
	accept_content=["json"],
	result_serializer="json",
	beat_schedule={
		"dispatch-scheduled-connector-syncs": {
			"task": "nexusbi.dispatch_scheduled_connector_syncs",
			"schedule": 300.0,
		}
	},
)
