from django.shortcuts import render
from django.shortcuts import render, redirect

from django.views import View

from shop.models import Product


class Basket(View):
    @staticmethod
    def get(request):
        ids = list(request.session.get('basket').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'shop/basket.html', {'products': products})


def index(request):
    return render(request, 'index.html')


def book_list(request):
    return render(request, 'shop/book_list.html')


def book_detail(request):
    return render(request, 'shop/book_detail.html')


