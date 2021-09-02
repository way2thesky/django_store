from django.shortcuts import render
from django.views import View

from orders.models import Order


class OrderView(View):
    @staticmethod
    def get(request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        return render(request, 'order/orders.html',
                      {'orders': orders})


