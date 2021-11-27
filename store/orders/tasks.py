import json

from celery import shared_task

from django.core.mail import send_mail as django_send_mail

from orders.models import Order

import requests


@shared_task
def send_mail(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order_id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                Your order id is {}.'.format(order.first_name,
                                             order.id)
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent


@shared_task
def send_to_api(title):
    data = {"title": title}
    data_json = json.dumps(data)
    print(data_json)  # noqa: T001
    requests.post('http://warehouse:8001/orders/', data_json)
