"""
The __init__.py file is used to initialize the backend package.
This app serves as the entry point for the Django project.
"""

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
