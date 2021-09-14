from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    exclude = ['id']
    list_display = ['name', 'code', 'balance']
    search_fields = ['name', 'code']
    ordering = ['id']

    def save_model(self, request, obj, form, change):
        if not obj.code:
            inventory = Inventory.objects.last()
            if inventory is not None:
                _id = inventory.code[2:]
            else:
                _id = '100'
            obj.code = 'I-' + str(int(_id)+1)
        super().save_model(request, obj, form, change)
