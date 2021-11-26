import json
from io import BytesIO

from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail as django_send_mail
from django.template.loader import render_to_string

from orders.models import Order

import requests

import weasyprint


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


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)

    # create invoice e-mail
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'admin@myshop.com',
                         [order.email])
    # generate PDF
    html = render_to_string('orders/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # send e-
    email.send()
