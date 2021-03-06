import hashlib
from urllib.parse import urlparse

from celery import shared_task

from django.core.files.base import ContentFile

import requests

from .models import Author, Book, Genre


@shared_task
def shop_sync():
    try:

        print('Starting update from warehouse api for database')  # noqa:T001
        print('Getting data from api...')  # noqa:T001

        url = 'http://warehouse:8001/genres/'
        print('Clearing data...')  # noqa:T001

        while url and (response_genres := requests.get(url)).status_code == requests.codes.ok:
            for genre_data in response_genres.json()['results']:
                Genre.objects.update_or_create(
                    slug=genre_data['slug'],
                    defaults={
                        'name': genre_data['name'],
                    }
                )
            url = response_genres.json()['next']

        url = 'http://warehouse:8001/authors/'
        print('Clearing data...')  # noqa:T001

        while url and (response_authors := requests.get(url)).status_code == requests.codes.ok:
            for author_data in response_authors.json()['results']:
                Author.objects.get_or_create(
                    id=author_data['id'],
                    defaults={
                        'slug': author_data['slug'],
                        'first_name': author_data['first_name'],
                        'last_name': author_data['last_name'],
                        'bio': author_data['bio']

                    }
                )
            url = response_authors.json()['next']

        url = 'http://warehouse:8001/books/'
        print('Clearing data...')  # noqa:T001
        while url and (response_books := requests.get(url)).status_code == requests.codes.ok:
            for book_data in response_books.json()['results']:
                book, created = Book.objects.update_or_create(
                    isbn=book_data['isbn'],
                    defaults={
                        'id': book_data['id'],
                        "author": Author.objects.get(id=book_data['author']),
                        "title": book_data['title'],
                        "description": book_data['description'],
                        "publication_year": book_data['publication_year'],

                        "language": book_data['language'],
                        "pages": book_data['pages'],
                        'slug': book_data['slug'],
                        "price": book_data['price'],
                        "created": book_data['created'],
                        "available": book_data['available'],
                        "quantity": book_data['quantity'],
                    }
                )

                image_name = urlparse(book_data['image']).path.split('/')[-1]
                img = requests.get(book_data['image']).content
                if not book.image:
                    book.image.save(image_name, ContentFile(img), save=True)
                else:
                    md5 = hashlib.md5()
                    for chunk in book.image.chunks():
                        md5.update(chunk)
                    if md5.hexdigest() != hashlib.md5(img).hexdigest():
                        book.image.save(image_name, ContentFile(img), save=True)

                for i in book_data['genre']:
                    genre = Genre.objects.get(id=i)
                    book.genre.add(genre)
                    book.save()

                url = response_books.json()['next']

    except Exception as e:
        print('Synchronization of two databases failed. See exception:')  # noqa:T001
        print(e)  # noqa:T001
    print('Database was updated from warehouse api')  # noqa:T001
