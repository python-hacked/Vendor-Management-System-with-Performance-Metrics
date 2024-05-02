from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_vendor_performance_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    vendor.update_performance_metrics()
