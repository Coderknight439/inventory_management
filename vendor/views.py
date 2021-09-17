from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import VendorForm
from django.contrib import messages
from .table import VendorTable
from .models import Vendor
import math


@login_required(login_url='/accounts/login/')
def index(request, **kwargs):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('per_page', 10))
    table = VendorTable(Vendor.objects.all())
    table.paginate(page=page, per_page=page_size)
    table.paginator.num_pages = math.ceil(table.paginator.count / table.paginator.per_page)
    table.page.number = page
    return render(request, 'vendor/index.html', {'table': table, 'title': 'Vendor List'})


@login_required(login_url='/accounts/login/')
def add(request, **kwargs):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, message="Vendor Added Successfully.")
            return redirect('vendor_index')
        else:
            messages.error(request, 'Vendor Could Not Be Added. Check error please.')
            return render(request, 'vendor/add.html', {'form': form, 'title': 'Vendor Add'})
    form = VendorForm
    return render(request, 'vendor/add.html', {'form': form, 'title': 'Vendor Add'})


@login_required(login_url='/accounts/login/')
def edit(request, vendor_id, **kwargs):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    form = VendorForm(instance=vendor)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, message="Vendor Updated Successfully.")
            return redirect('vendor_index')
    return render(request, 'vendor/add.html', {'form': form, 'title': 'Vendor Edit'})


@login_required(login_url='/accounts/login/')
def delete(request, vendor_id, **kwargs):
    if request.method == 'POST':
        try:
            instance = Vendor.objects.get(id=vendor_id)
            instance.delete()
            messages.success(request, message="Vendor Deleted Successfully.")
        except Exception:
            messages.error(request, message="Couldn't Delete!")
        return redirect('vendor_index')
    name = request.GET.get('name')
    return render(request, 'vendor/delete_confirm.html', {'name': name, 'title': 'Delete Vendor'})
