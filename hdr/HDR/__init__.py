"""init for FileHIMSyncService project.

it lets python know that this is a python directory
"""

from .celery import app as celery_app

__all__ = ['celery_app']