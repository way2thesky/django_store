from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect

from django.views import View

from shop.models import Product

from django.shortcuts import render, redirect, HttpResponseRedirect

from django.views import View


# class Index(View):
#     @staticmethod
#     def post(request, **kwargs):
#         product = request.POST.get('product')
#         remove = request.POST.get('remove')
#         basket = request.session.get('basket', {product: 1})
#         if basket:
#             quantity = basket.get(product)
#             if quantity:
#                 if remove:
#                     if quantity <= 1:
#                         basket.pop(product)
#                     else:
#                         basket[product] = quantity - 1
#                 else:
#                     basket[product] = quantity + 1
#
#         request.session['basket'] = basket
#         return redirect('index')
#
#     @staticmethod
#     def get(request):
#         return render(request, 'index.html')


def product_all(request):
    products = Product.products.all()
    return render(request, 'index.html', {'products': products})


def book_detail(request, slug=None):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'shop/book_detail.html', {'product': product})
