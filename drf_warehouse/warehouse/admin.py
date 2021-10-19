from django.contrib import admin

from .models import Order, OrderItem

from django.contrib import admin
from .models import Genre, Book, Author


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'created', 'status']
    list_filter = ['status']


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity', 'price']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['author', 'genre', 'title', 'slug', 'price',
                    'available', 'quantity']
    list_filter = ['available', 'created']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('title',)}
