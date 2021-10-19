import uuid

from django.contrib.auth.models import User

from django.db import models

from shop.models import Book


class Order(models.Model):
    class OrderStatus(models.IntegerChoices):
        WAITING = 1, 'Waiting'
        IN_PROGRESS = 2, 'In progress'
        SENT = 3, 'Sent'
        COMPLETED = 4, 'Completed'
        CANCELLED = 5, 'Cancelled from warehouse'

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    status = models.PositiveSmallIntegerField(
        choices=OrderStatus.choices, default=OrderStatus.WAITING)
    comment = models.CharField('comment', max_length=20, blank=True)

    def __str__(self):
        return f'{self.id}'

    def order_id(self):
        return self.id.__str__()


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    book = models.ForeignKey(Book,
                             related_name='order_items',
                             on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
