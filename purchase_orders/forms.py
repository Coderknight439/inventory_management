from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseOrder, OrderItems
from django.forms.models import BaseInlineFormSet


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ('vendor_id', 'inventory_id', 'purpose', )

    def clean(self):
        return super(PurchaseOrderForm, self).clean()


class OrderItemsForm(forms.ModelForm):
    class Meta:
        model = OrderItems
        fields = ('product_id', 'quantity', 'mrp', )


PurchaseOrderInlineFormset = inlineformset_factory(
    PurchaseOrder,
    OrderItems,
    form=OrderItemsForm,
    extra=1,
    can_delete_extra=False,
    can_delete=False
)


class PurchaseOrderInlineFormsetUpdate(BaseInlineFormSet):
    class Meta:
        model = OrderItems
        fields = ('product_id', 'quantity', 'mrp',)

    def initial_forms(self):
        import pdb; pdb.set_trace()
        return super(PurchaseOrderInlineFormsetUpdate, self).initial_forms()
