from django.db.models.signals import post_delete
from django.dispatch import receiver

from users.models import Customer


@receiver(post_delete, sender=Customer)
def delete_customer(sender, instance, **kwargs):
    instance.user.delete()
