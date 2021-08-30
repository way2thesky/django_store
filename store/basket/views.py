from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from django.views import View

from shop.models import Product


class Basket(View):
    @staticmethod
    def get(request):
        ids = list(request.session.get('basket').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'shop/basket.html', {'products': products})
