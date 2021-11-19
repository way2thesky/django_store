from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


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

    class Meta:
        ordering = ('name',)
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:book_list_by_genre', args=[self.slug])



class Book(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True)
    genre = models.ManyToManyField(Genre, blank=True, related_name='books', )
    publication_year = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    language = models.CharField("language", max_length=20)
    pages = models.IntegerField()
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    slug = models.SlugField(max_length=255, null=False, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    isbn = models.CharField('ISBN', max_length=13,
                            unique=True)
    rating = models.FloatField(default=0)
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
                       kwargs={'book_slug': self.slug})

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField(max_length=10000,
                               help_text="Input your comment.")
    rating = models.PositiveSmallIntegerField(
        choices=(
            (1, "★☆☆☆☆"),
            (2, "★★☆☆☆"),
            (3, "★★★☆☆"),
            (4, "★★★★☆"),
            (5, "★★★★★"),
        )

    )
