from celery import shared_task

from django.core.mail import send_mail

import requests
import json
from django.core.mail import send_mail as django_send_mail

from orders.models import Order
from shop.models import Author, Book, Genre


@shared_task
def send_order(first_name, last_name, phone_number, email, books):

    data = {
        "book": f"{books}",
        "email": f"{email}",
        "first_name": f"{first_name}",
        "last_name": f"{last_name}",
        "phone_number": f"{phone_number}",

    }
    requests.post(url='http://warehouse:8001/orders/', data=data)
