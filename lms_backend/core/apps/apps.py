from django.apps import AppConfig

## The only thing that I did here is configure signals. 

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals
