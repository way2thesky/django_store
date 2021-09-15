from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from orders.models import Order, OrderItem
from shop.models import Book
from .basket import Basket
from .forms import BasketAddBookForm


@require_POST
def basket_add(request, book_id):
    basket = Basket(request)
    book = get_object_or_404(Book, id=book_id)
    form = BasketAddBookForm(request.POST)
    if form.is_valid():
        item = form.cleaned_data
        basket.add(book=book,
                   quantity=item['quantity'],
                   override_quantity=item['override'])
    return redirect('basket:basket_detail')


@require_POST
def basket_remove(request, book_id):
    basket = Basket(request)
    book = get_object_or_404(Book, id=book_id)
    basket.remove(book)
    return redirect('basket:basket_detail')


def basket_detail(request):
    basket = Basket(request)
    for item in basket:
        item['update_quantity_form'] = BasketAddBookForm(initial={'quantity': item['quantity'],
                                                                  'override': True})
    return render(request, 'basket/basket_detail.html', {'basket': basket})
