from django.apps import AppConfig


class ExpenseConfig(AppConfig):
    name = 'expense'

    def ready(self):
        import expense.signals