from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Genre(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

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
    image = models.TextField(validators=[URLValidator()])
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    isbn = models.CharField('ISBN', max_length=13,
                            unique=True)
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    quantity = models.IntegerField()

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:book_detail',
                       args=[self.id, self.slug])
