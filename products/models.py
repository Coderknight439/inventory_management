from django.db import models
from inventory_journals.models import InventoryJournals
from django.db.models import Sum
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Product Name')
    code = models.CharField(max_length=256, verbose_name='Code', blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    sale_price = models.DecimalField(max_digits=15, decimal_places=4)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return '{}-{}'.format(self.name, self.code)

    def stock(self):
        data = InventoryJournals.objects.filter(product_id=self.id).aggregate(Sum('quantity'))['quantity__sum'] or 0
        return data
