from django.db import models

# Create your models here.
from inventories.models import Inventory


class InventoryJournals(models.Model):
    order_id = models.IntegerField(verbose_name='Order')
    product_id = models.IntegerField(verbose_name='Product')
    entry_date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    unit_cost = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    inventory_id = models.IntegerField(default=None, null=True, blank=True)

