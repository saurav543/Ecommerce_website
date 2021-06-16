from django.shortcuts import get_object_or_404, render
from django.urls.conf import include
from .models import Category, Product


def product_all(request):
    products = Product.objects.filter()
    return render(request, 'index.html', {'products': products})


def product_detail(request, slug):
    item = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'shop/products/single.html', {'item': item})


def category_list(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category__in=Category.objects.get(slug=slug).get_descendants(include_self=True))
    return render(request, 'shop/products/category.html', {'category': category, 'products': products})


    