from django.apps import AppConfig


class ShopordersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopOrders'

    def ready(self):
        import shopOrders.signals  # Импортируем сигнал
