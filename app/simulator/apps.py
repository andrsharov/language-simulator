"""
apps.py
"""

from django.apps import AppConfig


class SimulatorConfig(AppConfig):
    """
    Регистрирую приложение simulator
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simulator'
