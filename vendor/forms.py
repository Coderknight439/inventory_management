from django import forms
from .models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('name', 'address_line_1', 'address_line_2', 'contact_person', 'contact_number', 'email')

    def save(self, commit=True):
        if not self.instance.pk and not self.instance.vendor_id:
            vendor = Vendor.objects.last()
            if vendor is not None:
                _id = vendor.vendor_id[2:]
            else:
                _id = '100'
            self.instance.vendor_id = 'V-' + str(int(_id) + 1)
        return super(VendorForm, self).save(commit=commit)


