from django.apps import AppConfig

class TrainerAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trainer_auth'

    def ready(self):
        import trainer_auth.signals
