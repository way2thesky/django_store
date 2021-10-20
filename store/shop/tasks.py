from celery import shared_task

from django.core.mail import send_mail

import requests

from .models import Author, Book, Genre


@shared_task
def send_mail_task(subject, message, email):
    send_mail(subject, message, email, ['admin@example.com'])


@shared_task
def shop_sync():
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
            response_data_genre = requests.get(
                response_data_genre['next']
            ).json()
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
            book, created = Book.objects.get_or_create(
                id=data['id'],
                defaults={
                    'id': data['id'],
                    "genre": Genre.objects.get(id=data['genre']),
                    "title": data['title'],
                    "description": data['description'],
                    "language": data['language'],
                    "pages": data['pages'],
                    "image": data['image'],
                    'slug': data['slug'],
                    "price": data['price'],
                    "isbn": data['isbn'],
                    "created": data['created'],
                    "available": data['available'],
                    "quantity": data['quantity'],
                    "author": Author.objects.get(id=data['author'])
                }
            )

            if not created:
                book.genre = Genre.objects.get(id=data['genre'])

                book.title = data['title']
                book.description = data['description']
                book.language = data['language']
                book.pages = data['pages']
                book.image = data['image']
                book.slug = data['slug']
                book.price = data['price']
                book.isbn = data['isbn']
                book.created = data['created']
                book.available = data['available']
                book.quantity = data['quantity']
                book.author = Author.objects.get(id=data['author'])
                book.save()

        if response_data_book['next']:
            response_data_book = requests.get(response_data_book['next']).json()
        else:
            break
    print('Database was updated from warehouse api')
