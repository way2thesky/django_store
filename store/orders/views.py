from django.shortcuts import render

from basket.basket import Basket
from .models import OrderItem
from .forms import OrderItemsForm


def order_create(request):
    basket = Basket(request)
    user = request.user
    if request.method == 'POST':
        form = OrderItemsForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user
            order.save()
            for item in basket:
                OrderItem.objects.create(order=order,
                                         book=item['book'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                item['book'].quantity = item['book'].quantity - item['quantity']
                item['book'].save()
            basket.clear()

            return render(request,
                          'orders/order_created.html',
                          {'order': order})
    else:
        form = OrderItemsForm()
    return render(request,
                  'orders/order_create.html',
                  {'basket': basket, 'form': form})
