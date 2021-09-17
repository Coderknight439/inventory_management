from django.contrib.auth.models import User
from django.db import models
from vendor.models import Vendor
from products.models import Product
from inventories.models import Inventory
from django.core.exceptions import ValidationError


STATUS_CHOICES = [
    (0, 'Pending'),
    (1, 'Completed'),
    (2, 'Rejected'),
]


class PurchaseOrder(models.Model):
    order_number = models.CharField(max_length=256, verbose_name='Order No.')
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Vendor')
    inventory_id = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name='Inventory', default=None, null=True)
    purpose = models.TextField(max_length=1024, verbose_name='Purpose')
    entry_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    def __str__(self):
        return '{}'.format(self.order_number)

    class Meta:
        db_table = 'purchase_invoice'
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"

    def update_total_amount(self):
        total = 0
        for p in self.orderitems_set.all():
            raw_total = float(p.quantity * p.mrp)
            total += raw_total
        self.amount = total
        self.save()

    def status_text(self):
        status_string = ''
        for val in STATUS_CHOICES:
            if val[0] == self.status:
                status_string = val[1]
                break
        return status_string

    def clean(self):
        if not self.inventory_id:
            raise ValidationError("Please Select an Inventory")


class OrderItems(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=256, verbose_name='Product')
    purchase_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='order')
    quantity = models.IntegerField(default=1)
    mrp = models.DecimalField(max_digits=15, decimal_places=4)

    class Meta:
        db_table = 'order_items'
