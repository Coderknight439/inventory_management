from django.db import models
from django.db.models import Sum

# Create your models here.

class Inventory(models.Model):
    name = models.CharField(max_length=256, verbose_name='Name')
    code = models.CharField(max_length=256, verbose_name='Code', blank=True, null=True)

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"

    def __str__(self):
        return '{}-{}'.format(self.name, self.code)

    def balance(self):
        from inventory_journals.models import InventoryJournals
        data = InventoryJournals.objects.filter(inventory_id=self.id).aggregate(Sum('total'))['total__sum'] or 0
        return data
