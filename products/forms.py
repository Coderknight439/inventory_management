from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'purchase_price', 'sale_price')

    def save(self, commit=True):
        if not self.instance.pk and not self.instance.code:
            product = Product.objects.last()
            if product is not None:
                _id = product.code[2:]
            else:
                _id = '100'
            self.instance.code = 'P-' + str(int(_id) + 1)
        return super(ProductForm, self).save(commit=commit)


