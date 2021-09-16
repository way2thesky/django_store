from celery import shared_task

from django.core.mail import send_mail

import requests

from .models import Author, Book, Genre


@shared_task
def send_mail_task(subject, message, email):
    send_mail(subject, message, email, ['admin@example.com'])


@shared_task
def shop_sync():
    url = 'http://127.0.0.1:8000/warehouse/authors/'
    response_author = requests.get(url).json()
    while 1:
        for counter, data in enumerate(response_author['results']):
            Author.objects.get_or_create(
                id=data['id'],
                defaults={
                    'id': data['id'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name']
                }
            )

        if response_author['next']:
            response_author = requests.get(response_author['next']).json()
        else:
            break

    url = 'http://127.0.0.1:8000/warehouse/genres/'
    response_genre = requests.get(url).json()
    while 1:
        for counter, data in enumerate(response_genre['results']):
            Genre.objects.get_or_create(
                id=data['id'],
                defaults={
                    'id': data['id'],
                    'name': data['name']
                }
            )

        if response_genre['next']:
            response_genre = requests.get(
                response_genre['next']
            ).json()
        else:
            break

    url = 'http://127.0.0.1:8000/warehouse/books/'
    response = requests.get(url).json()
    while 1:
        for counter, data in enumerate(response['results']):
            book, created = Book.objects.get_or_create(
                id=data['id'],
                defaults={
                    'id': data['id'],
                    "title": data['title'],
                    "description": data['description'],
                    "image": data['image'],
                    "language": data['language'],
                    "status": data['status'],
                    "price": data['price'],
                    "isbn": data['isbn'],
                    "pages": data['pages'],
                    "created": data['created'],
                    "available": data['available'],
                    "quantity": data['quantity'],
                    "genre": Genre.objects.get(id=data['genre'])
                }
            )

            if not created:
                book.title = data['title']
                book.description = data['description']
                book.image = data['image']
                book.language = data['language']
                book.status = data['status']
                book.price = data['price']
                book.isbn = data['isbn']
                book.pages = data['pages']
                book.created = data['created']
                book.available = data['available']
                book.quantity = data['quantity']
                book.genre = Genre.objects.get(id=data['genre'])
                book.save()

            for i in data['author']:
                author = Author.objects.get(id=i)
                book.author.add(author)

        if response['next']:
            response = requests.get(response['next']).json()
        else:
            break
