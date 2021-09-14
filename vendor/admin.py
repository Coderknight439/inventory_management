from django.contrib import admin
from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    exclude = ['vendor_id']
    list_display = ['name', 'contact_person', 'contact_number', 'address_line_1', 'email']
    list_editable = ['contact_number', 'address_line_1', 'email']
    search_fields = ['name']
    ordering = ['id']

    def save_model(self, request, obj, form, change):
        if obj.vendor_id == '':
            vendor = Vendor.objects.last()
            if vendor is not None:
                _id = vendor.vendor_id[2:]
            else:
                _id = '100'
            obj.vendor_id = 'V-' + str(int(_id)+1)
        super().save_model(request, obj, form, change)
