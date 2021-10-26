import os
import tempfile
from os.path import basename

from celery import shared_task
import tempfile

import requests
from django.core import files
from django.core.files.base import ContentFile, File
from django.core.files.temp import NamedTemporaryFile

from .models import Author, Book, Genre


@shared_task
def shop_sync():
    try:
        print('Starting update from warehouse api for database')
        print('Getting data from api...')

        url = 'http://warehouse:8001/authors/'
        print('Clearing data...')

        response_author = requests.get(url)
        if response_author.status_code != 200:
            return
        response_data_author = response_author.json()
        while 1:
            for counter, data in enumerate(response_data_author['results']):
                Author.objects.get_or_create(
                    id=data['id'],
                    defaults={
                        'id': data['id'],
                        'first_name': data['first_name'],
                        'last_name': data['last_name']
                    }
                )

            if response_data_author['next']:
                response_data_author = requests.get(response_data_author['next']).json()
            else:
                break

        url = 'http://warehouse:8001/genres/'
        print('Clearing data...')

        response_genre = requests.get(url)
        if response_genre.status_code != 200:
            return
        response_data_genre = response_genre.json()

        while 1:
            for counter, data in enumerate(response_data_genre['results']):
                Genre.objects.get_or_create(
                    id=data['id'],
                    defaults={
                        'slug': data['slug'],
                        'name': data['name'],
                    }
                )

            if response_data_genre['next']:
                response_data_genre = requests.get(response_data_genre['next']).json()
            else:
                break

        url = 'http://warehouse:8001/books/'
        print('Clearing data...')

        response_book = requests.get(url)
        if response_book.status_code != 200:
            return
        response_data_book = response_book.json()

        while 1:
            for counter, data in enumerate(response_data_book['results']):
                r = requests.get(data['image'])
                if r.status_code != requests.codes.ok:
                    continue
                image_temp = tempfile.NamedTemporaryFile()
                for block in r.iter_content(1024 * 8):
                    if not block:
                        break
                    image_temp.write(block)

                # куда эту строку нужно передать, если мне нужен book.image (image_temp)
                # Local variable 'book' might be referenced before assignment
                book.image.save(basename(data['image']), files.File(image_temp))

                book, created = Book.objects.get_or_create(
                    # image_temp.book.save(basename(data['image']), files.File(image_temp)),
                    id=data['id'],
                    defaults={
                        'id': data['id'],
                        "genre": Genre.objects.get(id=data['genre']),
                        "author": Author.objects.get(id=data['author']),
                        "title": data['title'],
                        "description": data['description'],
                        "language": data['language'],
                        "pages": data['pages'],
                        'slug': data['slug'],
                        "price": data['price'],
                        "isbn": data['isbn'],
                        "created": data['created'],
                        "available": data['available'],
                        "quantity": data['quantity'],
                    }
                )
                # r = requests.get(data['image'])
                # if r.status_code != requests.codes.ok:
                #     continue
                # lf = tempfile.NamedTemporaryFile()
                # for block in r.iter_content(1024 * 8):
                #     if not block:
                #         break
                #     lf.write(block)
                # book.image.save(basename(data['image']), files.File(lf))

                # есть такой еще вариант
                # r = requests.get(data['image'])
                # if r.ok:
                #     book.image.save(basename(data['image']), ContentFile(r.content))
                if not created:
                    book.genre = Genre.objects.get(id=data['genre'])
                    book.author = Author.objects.get(id=data['author'])
                    book.title = data['title']
                    book.description = data['description']
                    book.language = data['language']
                    book.pages = data['pages']
                    book.slug = data['slug']
                    book.price = data['price']
                    book.isbn = data['isbn']
                    book.created = data['created']
                    book.available = data['available']
                    book.quantity = data['quantity']
                    book.save()

            if response_data_book['next']:
                response_data_book = requests.get(response_data_book['next']).json()
            else:
                break
        print('Database was updated from warehouse api')

    except Exception as e:
        print('Synchronization of two databases failed. See exception:')  # noqa:T001
        print(e)  # noqa:T001

# import requests
# import tempfile
# from shop.models import Book
# from django.core import files
#
# # List of images to download
# obj = Book.objects.create()
# link = 'http://warehouse:8001/books/'
# r = requests.get(link).json()
# if r.ok:
#     obj.file_field.save(os.path.basename(link), ContentFile(r.content))
