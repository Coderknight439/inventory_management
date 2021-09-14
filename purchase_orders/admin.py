from django.contrib import admin
from .models import *
from django.contrib import messages
from inventory_journals.models import InventoryJournals


class ProductInline(admin.TabularInline):
    model = OrderItems
    extra = 1
    can_delete = True
    fields = ['product_id', 'quantity', 'mrp']

    def get_formset(self, request, obj=None, **kwargs):
        if obj and obj.id:
            self.extra = 0
        return super(ProductInline, self).get_formset(request, obj=obj, **kwargs)


@admin.action(description='Mark selected orders as completed')
def make_completed(modeladmin, request, queryset):
    count = 0
    for index, order in enumerate(queryset):
        if order.status == STATUS_CHOICES[0][0]:
            for product in order.orderitems_set.all():
                journal_data = InventoryJournals(
                    order_id=order.id,
                    inventory_id=order.inventory_id.id,
                    product_id=product.product_id.id,
                    quantity=product.quantity,
                    unit_cost=product.mrp,
                    total=product.quantity * product.mrp,
                )
                journal_data.save()
        else:
            queryset.pop(index)
            count += 1
    updated = queryset.update(status=STATUS_CHOICES[1][0])
    modeladmin.message_user(request, '{updated} Purchase Orders are Marked as Completed. {count} are in Invalid State'.format(updated=updated, count=count), messages.SUCCESS)


@admin.action(description='Mark selected orders as rejected')
def make_rejected(modeladmin, request, queryset):
    count = 0
    for index, order in enumerate(queryset):
        if order.status != STATUS_CHOICES[0][0]:
            count += 1
            queryset.pop(index)
    updated = queryset.update(status=STATUS_CHOICES[2][0])
    order_id_list = [obj.id for obj in queryset]
    InventoryJournals.objects.filter(order_id__in=order_id_list).delete()
    modeladmin.message_user(request, '{updated} Purchase Orders are Marked as Rejected. {count} are in Invalid State'.format(updated=updated, count=count), messages.SUCCESS)


@admin.action(description='Mark selected orders as pending')
def make_pending(modeladmin, request, queryset):
    updated = queryset.update(status=STATUS_CHOICES[0][0])
    order_id_list = [obj.id for obj in queryset]
    InventoryJournals.objects.filter(order_id__in=order_id_list).delete()
    modeladmin.message_user(request, '{updated} Purchase Orders are Marked as Pending'.format(updated=updated), messages.SUCCESS)


@admin.register(PurchaseOrder)
class PurchaseInvoiceAdmin(admin.ModelAdmin):
    exclude = ['entry_date', 'amount', 'created_by', 'order_number', 'status']
    list_display = ['order_number', 'vendor_id', 'entry_date', 'amount', 'status_text']
    search_fields = ['order_number']
    list_filter = ['status']
    inlines = [
        ProductInline
    ]
    ordering = ['id']
    actions = [make_pending, make_completed, make_rejected]
    # filter_horizontal =['']

    class Media:
        js = ('js/admin/purchase_order_admin.js',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        obj.amount = 0
        if not obj.id:
            purchase = PurchaseOrder.objects.last()
            if purchase is not None:
                purchase_id = int(purchase.order_number[3:])+1
            else:
                purchase_id = 101
            obj.order_number = 'PO-' + str(purchase_id)
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
            instance.purchase_id.update_total_amount()
        formset.save_m2m()

    def has_change_permission(self, request, obj=None):
        if obj and obj.status != STATUS_CHOICES[0][0]:
            return False
        return super(PurchaseInvoiceAdmin, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status != STATUS_CHOICES[0][0]:
            return False
        return super(PurchaseInvoiceAdmin, self).has_delete_permission(request, obj)
