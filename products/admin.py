from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ['id']
    list_display = ['name', 'code', 'purchase_price', 'sale_price', 'stock']
    list_editable = ['sale_price']
    search_fields = ['name', 'code']
    ordering = ['id']

    class Media:
        js = ('js/admin/product_admin.js',)

    def save_model(self, request, obj, form, change):
        if not obj.code:
            product = Product.objects.last()
            if product is not None:
                _id = product.code[2:]
            else:
                _id = '100'
            obj.code = 'P-' + str(int(_id)+1)
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.id:
            self.exclude.append('code')
        form = super().get_form(request, obj, **kwargs)
        return form
