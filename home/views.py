from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from products.models import Product
from inventories.models import Inventory
from vendor.models import Vendor
from purchase_orders.models import PurchaseOrder


@login_required(login_url='/accounts/login/')
def index(request, **kwargs):
    product_count = Product.objects.all().count()
    vendor_count = Vendor.objects.all().count()
    inventory_count = Inventory.objects.all().count()
    order_count = PurchaseOrder.objects.all().count()
    return render(request, 'home/index.html', {
        'title': 'Home',
        'product_count': product_count,
        'vendor_count': vendor_count,
        'inventory_count': inventory_count,
        'order_count': order_count,
    }
                  )
