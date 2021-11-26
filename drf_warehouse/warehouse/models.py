from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, null=False, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('shop:author_detail',
                       kwargs={'author_slug': self.slug})


class Genre(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:book_list_by_genre', args=[self.slug])


class Book(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True)
    genre = models.ManyToManyField(Genre, blank=True, verbose_name="genre")
    publication_year = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    language = models.CharField("language", max_length=20)
    pages = models.IntegerField()
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    isbn = models.CharField('ISBN', max_length=13,
                            unique=True)
    rating = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.title

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])


class Order(models.Model):
    class OrderStatus(models.IntegerChoices):
        WAITING = 1, 'Waiting'
        IN_PROGRESS = 2, 'In progress'
        SENT = 3, 'Sent'
        COMPLETED = 4, 'Completed'
        CANCELLED = 5, 'Cancelled from warehouse'

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    order_date = models.DateField('order date', null=True, blank=True, help_text='Date when order was created')

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
