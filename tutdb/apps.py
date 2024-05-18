from django.apps import AppConfig


class TutdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tutdb'

    def ready(self):
        import tutdb.signals
