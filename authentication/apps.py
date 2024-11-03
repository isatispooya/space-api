from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        from .superuser import create_superuser_if_not_exists
        create_superuser_if_not_exists('1231231231', '1231231231@example.com', '123456', '1992-01-13')
