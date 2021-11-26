import json

from celery import shared_task

import requests

from orders.models import Order
from django.core.mail import send_mail as django_send_mail


@shared_task
def send_mail(order_id):
    order = Order.objects.get(id=order_id)
    message = f'Dear {order.first_name}, in this message we will give you some info about your order'

    django_send_mail('Info about your order', message, 'test@testmail.com', [order.email])


@shared_task
def send_to_api(title):
    data = {"title": title}
    data_json = json.dumps(data)
    print(data_json)  # noqa: T001
    requests.post('http://warehouse:8001/orders/', data_json)
