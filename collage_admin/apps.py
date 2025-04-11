from django.apps import AppConfig


class CollageAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collage_admin'

    def ready(self):
        import collage_admin.signals
