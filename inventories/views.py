from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import InventoryForm
from django.contrib import messages
from .table import InventoryTable
from .models import Inventory
import math


@login_required(login_url='/accounts/login/')
def index(request, **kwargs):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('per_page', 10))
    table = InventoryTable(Inventory.objects.all())
    table.paginate(page=page, per_page=page_size)
    table.paginator.num_pages = math.ceil(table.paginator.count / table.paginator.per_page)
    table.page.number = page
    return render(request, 'inventory/index.html', {'table': table, 'title': 'Inventory List'})


@login_required(login_url='/accounts/login/')
def add(request, **kwargs):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, message="Inventory Added Successfully.")
            return redirect('inventory_index')
        else:
            messages.error(request, 'Inventory Could Not Be Added. Check error please.')
            return render(request, 'inventory/add.html', {'form': form, 'title': 'Inventory Add'})
    form = InventoryForm
    return render(request, 'inventory/add.html', {'form': form, 'title': 'Inventory Add'})


@login_required(login_url='/accounts/login/')
def edit(request, inventory_id, **kwargs):
    inventory = get_object_or_404(Inventory, pk=inventory_id)
    form = InventoryForm(instance=inventory)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, message="Inventory Updated Successfully.")
            return redirect('inventory_index')
    return render(request, 'inventory/add.html', {'form': form, 'title': 'Inventory Edit'})


@login_required(login_url='/accounts/login/')
def delete(request, inventory_id, **kwargs):
    if request.method == 'POST':
        try:
            instance = Inventory.objects.get(id=inventory_id)
            instance.delete()
            messages.success(request, message="Inventory Deleted Successfully.")
        except Exception:
            messages.error(request, message="Couldn't Delete!")
        return redirect('inventory_index')
    name = request.GET.get('name')
    return render(request, 'inventory/delete_confirm.html', {'name': name, 'title': 'Delete Inventory'})
