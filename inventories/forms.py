from django import forms
from .models import Inventory


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('name', )

    def save(self, commit=True):
        if not self.instance.pk and not self.instance.code:
            inventory = Inventory.objects.last()
            if inventory is not None:
                _id = inventory.code[2:]
            else:
                _id = '100'
            self.instance.code = 'I-' + str(int(_id) + 1)
        return super(InventoryForm, self).save(commit=commit)


