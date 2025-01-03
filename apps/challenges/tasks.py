# tasks.py
import time
from celery import shared_task


@shared_task
def send_interaction_notification(interaction_id):
    """
    Example of a simple Celery task that gets triggered after an Interaction
    is created.
    TODO: Implement the actual task logic.
    """
    # Do something with the interaction_id, e.g., send a notification email,
    # update analytics, etc.

    time.sleep(10)  # Simulate a long-running task
    return {
        'id': interaction_id,
    }
