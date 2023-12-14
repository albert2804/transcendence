from django.apps import AppConfig


class TestDbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_db'
