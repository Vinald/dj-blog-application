from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        # Import signal handlers to ensure they are registered
        pass
        import account.signals
