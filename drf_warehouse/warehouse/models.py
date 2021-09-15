from django.urls import reverse
import uuid
from django.contrib.auth.models import User

from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Genre(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:book_list_by_genre', args=[self.slug])


class Book(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre,
                              related_name='books',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    language = models.CharField("language", max_length=20)
    pages = models.IntegerField()
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    isbn = models.CharField('ISBN', max_length=13,
                            unique=True)
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.title


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

