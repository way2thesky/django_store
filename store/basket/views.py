from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from shop.models import Book

from .basket import Basket
from .cart import Cart
from .forms import BasketAddBookForm


def basket_update(request, book_id):
    basket = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = BasketAddBookForm(data=request.POST, product=book, cart=basket)
    if form.is_valid():
        item = form.cleaned_data
        basket.add(book=book,
                   quantity=item['quantity'],
                   override_quantity=item['override'])
        messages.success(request, "Item added to the cart!")

    else:
        messages.error(request, "too many books: Check in Stock")

        print(form.errors)   # noqa:T001
    return redirect('basket:basket_detail')


def basket_add(request, book_id):
    basket = Basket(request)
    book = get_object_or_404(Book, id=book_id)
    basket.add(book=book)

    return redirect(book)


def basket_detail(request):
    basket = Cart(request)
    for item in basket:
        item['update_quantity_form'] = BasketAddBookForm(initial={'quantity': item['quantity'],
                                                                  'override': True}, cart=basket,
                                                         product=Book.objects.get(id=item["pk"]))
    return render(request, 'basket/basket_detail.html', {'basket': basket})


def basket_remove(request, book_id):
    basket = Basket(request)
    book = get_object_or_404(Book, id=book_id)
    basket.remove(book)
    return redirect('basket:basket_detail')


def basket_summary(request):
    return render(request, 'basket/summary.html')
