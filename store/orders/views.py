import json

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect
import requests
from .tasks import send_mail_task, send_mail
from basket.basket import Basket
from .models import OrderItem, Order
from .forms import OrderItemsForm


def order_create(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = OrderItemsForm(request.POST)
        if form.is_valid():
            # check quantity for every item in basket
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in basket:
                OrderItem.objects.create(order=order,
                                         book=item['book'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                item['book'].quantity = item['book'].quantity - item['quantity']
                item['book'].save()

                send_mail_task.delay(str(item['book']))
            send_mail.delay(order.id)
            basket.clear()

            return render(request,
                          'orders/order_created.html',
                          {'order': order})
    else:
        form = OrderItemsForm()
    return render(request,
                  'orders/order_create.html',
                  {'basket': basket, 'form': form})