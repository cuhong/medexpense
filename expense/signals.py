from django.db.models.signals import post_save
from django.dispatch import receiver

from expense.models import Claim, Expense


@receiver(post_save, sender=Claim)
def claim_post_save(sender, instance, created, **kwargs):
    instance.set_serial()


@receiver(post_save, sender=Expense)
def expense_post_save(sender, instance, created, **kwargs):
    instance.set_serial()
