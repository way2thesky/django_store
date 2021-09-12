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
#         cart = request.session.get('cart', {product: 1})
#         if cart:
#             quantity = cart.get(product)
#             if quantity:
#                 if remove:
#                     if quantity <= 1:
#                         cart.pop(product)
#                     else:
#                         cart[product] = quantity - 1
#                 else:
#                     cart[product] = quantity + 1
#
#         request.session['cart'] = cart
#         return redirect('index')
#
#     @staticmethod
#     def get(request):
#         return render(request, 'index.html')
#

def product_all(request):
    products = Product.products.all()
    return render(request, 'index.html', {'products': products})


# def book_detail(request, slug=None):
#     product = get_object_or_404(Product, slug=slug, in_stock=True)
#     return render(request, 'shop/book_detail.html', {'product': product})

def book_detail(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None



    data = {}
    data['products'] = products


    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', data)