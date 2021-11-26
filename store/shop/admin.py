from django.contrib import admin

from .models import Author, Book, Genre


class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    inlines = [BooksInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'slug', 'price',
                    'available', 'quantity', 'display_genre')
    list_filter = ['available', 'created']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Genre)