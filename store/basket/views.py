from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
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
    form = BasketAddBookForm(data=request.POST, product=book, cart=basket)
    if form.is_valid():
        item = form.cleaned_data
        basket.add(book=book,
                   quantity=item['quantity'],
                   override_quantity=item['override'])
        messages.success(request, "Item added to the cart!")

    else:
        # add error message using django messages
        messages.error(request, "TOO MANY BOOKS")

        print(form.errors)
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
                                                                  'override': True}, cart=basket,
                                                         product=Book.objects.get(id=item["pk"]))
    return render(request, 'basket/basket_detail.html', {'basket': basket})
