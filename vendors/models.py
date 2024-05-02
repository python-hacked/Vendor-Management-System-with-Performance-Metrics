from django.db import models
from django.db.models import Count, Avg
from django.utils import timezone

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    

    def update_performance_metrics(self):
        # Calculate On-Time Delivery Rate
        completed_orders_count = self.purchaseorder_set.filter(status='completed').count()
        if completed_orders_count > 0:
            on_time_delivery_count = self.purchaseorder_set.filter(status='completed', delivery_date__lte=timezone.now()).count()
            self.on_time_delivery_rate = (on_time_delivery_count / completed_orders_count) * 100
        else:
            self.on_time_delivery_rate = 0

        # Calculate Quality Rating Average
        completed_orders_with_rating = self.purchaseorder_set.filter(status='completed').exclude(quality_rating__isnull=True)
        self.quality_rating_avg = completed_orders_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0

        # Calculate Average Response Time
        acknowledged_orders = self.purchaseorder_set.filter(status='completed').exclude(acknowledgment_date__isnull=True)
        response_times = [(order.acknowledgment_date - order.issue_date).total_seconds() for order in acknowledged_orders]
        self.average_response_time = sum(response_times) / len(response_times) if response_times else 0

        # Calculate Fulfilment Rate
        fulfilled_orders_count = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False).count()
        issued_orders_count = self.purchaseorder_set.count()
        if issued_orders_count > 0:
            self.fulfillment_rate = (fulfilled_orders_count / issued_orders_count) * 100
        else:
            self.fulfillment_rate = 0

        # Save updated performance metrics
        self.save()


class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    )

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
