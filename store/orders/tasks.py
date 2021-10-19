from celery import shared_task

from django.core.mail import send_mail

import requests
import json
from django.core.mail import send_mail as django_send_mail

from orders.models import Order
from shop.models import Author, Book, Genre


@shared_task
def send_mail(id):
    order = Order.objects.get(id=id)
    message = f'Dear {order.first_name}, in this message we will give you some info about your order'

    django_send_mail('Info about your order', message, 'test@testmail.com', [order.email])


@shared_task
def send_mail_task(name):
    data = {"name": name}
    data_json = json.dumps(data)
    print(data_json)
    requests.post('http://warehouse:8001/recieve/', data_json)
