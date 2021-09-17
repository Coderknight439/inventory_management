from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.contrib import messages
from .table import ProductTable
from .models import Product
import math


@login_required(login_url='/accounts/login/')
def index(request, **kwargs):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('per_page', 10))
    table = ProductTable(Product.objects.all())
    table.paginate(page=page, per_page=page_size)
    table.paginator.num_pages = math.ceil(table.paginator.count / table.paginator.per_page)
    table.page.number = page
    return render(request, 'product/index.html', {'table': table, 'title': 'Product List'})


@login_required(login_url='/accounts/login/')
def add(request, **kwargs):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, message="Product Added Successfully.")
            return redirect('product_index')
        else:
            messages.error(request, 'Product Could Not Be Added. Check error please.')
            return render(request, 'product/add.html', {'form': form, 'title': 'Product Add'})
    form = ProductForm
    return render(request, 'product/add.html', {'form': form, 'title': 'Product Add'})


@login_required(login_url='/accounts/login/')
def edit(request, product_id, **kwargs):
    product = get_object_or_404(Product, pk=product_id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, message="Product Updated Successfully.")
            return redirect('product_index')
    return render(request, 'product/add.html', {'form': form, 'title': 'Product Edit'})

