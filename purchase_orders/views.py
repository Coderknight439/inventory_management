from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required

from inventory_journals.models import InventoryJournals
from .forms import PurchaseOrderInlineFormset, PurchaseOrderForm
from django.contrib import messages
from .table import PurchaseOrderTable
from .models import PurchaseOrder, OrderItems
import math
from django.http import JsonResponse


@login_required(login_url='/accounts/login/')
def index(request, **kwargs):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('per_page', 10))
    table = PurchaseOrderTable(PurchaseOrder.objects.all())
    table.paginate(page=page, per_page=page_size)
    table.paginator.num_pages = math.ceil(table.paginator.count / table.paginator.per_page)
    table.page.number = page
    return render(request, 'purchase_order/index.html', {'table': table, 'title': 'Purchase Order List'})


@login_required(login_url='/accounts/login/')
def add(request, **kwargs):
    if request.is_ajax():
        cp = request.POST.copy()
        value = int(cp['wtd'])
        prefix = "order"
        cp[f'{prefix}-TOTAL_FORMS'] = int(
            cp[f'{prefix}-TOTAL_FORMS']) + value
        formset = PurchaseOrderInlineFormset(cp)
        return render(request, 'purchase_order/formset.html', {'inline_form': formset})
    if request.method == 'POST':
        amount = 0
        inline_form = PurchaseOrderInlineFormset(request.POST)
        if inline_form.is_valid():
            for subform in inline_form:
                amount += subform.cleaned_data.get('mrp', 0)
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            purchase = PurchaseOrder.objects.last()
            if purchase is not None:
                purchase_id = int(purchase.order_number[3:]) + 1
            else:
                purchase_id = 101
            order_number = 'PO-' + str(purchase_id)
            model = PurchaseOrder(
                id=None,
                entry_date='',
                vendor_id=form.cleaned_data.get('vendor_id'),
                inventory_id=form.cleaned_data.get('inventory_id'),
                purpose=form.cleaned_data.get('purpose'),
                amount=amount,
                created_by=request.user,
                order_number=order_number,
                status=0
            )
            model.save()
            for subform in inline_form:
                subform.cleaned_data.pop('purchase_id')
                item = OrderItems(purchase_id=model, **subform.cleaned_data)
                item.save()
            messages.success(request, message="Purchase Order Added Successfully.")
            return redirect('order_index')
        else:
            messages.error(request, 'Purchase Order Could Not Be Added. Check error please.')
            return render(request, 'purchase_order/add.html', {'form': form, 'title': 'Add Purchase Order'})
    inline_form = PurchaseOrderInlineFormset
    form = PurchaseOrderForm
    return render(request, 'purchase_order/add.html', {'form': form, 'inline_form': inline_form, 'title': 'Add Purchase Order'})


@login_required(login_url='/accounts/login/')
def pending(request, order_id, **kwargs):
    purchase_order = PurchaseOrder.objects.get(pk=order_id)
    if request.method == 'POST':
        if purchase_order.status == 0:
            messages.info(request, message='Order is Already Pending')
        else:
            InventoryJournals.objects.filter(order_id=order_id).delete()
            purchase_order.status = 0
            purchase_order.save()
            messages.success(request, message="Order status changed to pending successfully")
        return redirect('order_index')
    status_text = 'Pending'
    return render(request, 'purchase_order/status_confirm.html', {'order': purchase_order,'status_text': status_text, 'title': 'Change Status'})


@login_required(login_url='/accounts/login/')
def complete(request, order_id, **kwargs):
    purchase_order = PurchaseOrder.objects.get(pk=order_id)
    if request.method == 'POST':
        if purchase_order.status == 1:
            messages.info(request, message='Order is Already Complete')
        elif purchase_order.status == 2:
            messages.error(request, message='Reject to Complete is not Allowed')
        else:
            for product in purchase_order.order.all():
                journal_data = InventoryJournals(
                    order_id=purchase_order.id,
                    inventory_id=purchase_order.inventory_id.id,
                    product_id=product.product_id.id,
                    quantity=product.quantity,
                    unit_cost=product.mrp,
                    total=product.quantity * product.mrp,
                )
                journal_data.save()
            purchase_order.status = 1
            purchase_order.save()
            messages.success(request, message="Order status changed to complete successfully")
        return redirect('order_index')
    status_text = 'Complete'
    return render(request, 'purchase_order/status_confirm.html',
                  {'order': purchase_order, 'status_text': status_text, 'title': 'Change Status'})


@login_required(login_url='/accounts/login/')
def reject(request, order_id, **kwargs):
    purchase_order = PurchaseOrder.objects.get(pk=order_id)
    if request.method == 'POST':
        if purchase_order.status == 1:
            messages.error(request, message='Complete to Reject is not Allowed')
        else:
            purchase_order.status = 2
            purchase_order.save()
            messages.success(request, message="Order status changed to rejected successfully")
        return redirect('order_index')
    status_text = 'Reject'
    return render(request, 'purchase_order/status_confirm.html',
                  {'order': purchase_order, 'status_text': status_text, 'title': 'Change Status'})


@login_required(login_url='/accounts/login/')
def view(request, order_id, **kwargs):
    purchase_order = PurchaseOrder.objects.get(pk=order_id)
    return render(request, 'purchase_order/view.html',
                  {'order': purchase_order, 'title': 'Order View'})