from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.conf import settings

        x_frame_middleware = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
        if x_frame_middleware not in settings.MIDDLEWARE:
            settings.MIDDLEWARE.append(x_frame_middleware)
