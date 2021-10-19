from celery import shared_task

from django.core.mail import send_mail

import requests

from .models import Author, Book, Genre


@shared_task
def send_mail_task(subject, message, email):
    send_mail(subject, message, email, ['admin@example.com'])


# @shared_task
# def shop_sync():
#     url = 'http://warehouse:8001/warehouse/authors/'
#     response_author = requests.get(url)
#     if response_author.status_code != 200:
#         return
#     response_data = response_author.json()
#     while 1:
#         for counter, data in enumerate(response_data['results']):
#             Author.objects.get_or_create(
#                 id=data['id'],
#                 defaults={
#                     'id': data['id'],
#                     'first_name': data['first_name'],
#                     'last_name': data['last_name']
#                 }
#             )
#
#         if response_data['next']:
#             response_data = requests.get(response_data['next']).json()
#         else:
#             break
#
#     url = 'http://warehouse:8001/warehouse/genres/'
#     response_genre = requests.get(url)
#     if response_genre.status_code != 200:
#         return
#     response_data_genre = response_genre.json()
#
#     while 1:
#         for counter, data in enumerate(response_data_genre['results']):
#             Genre.objects.get_or_create(
#                 id=data['id'],
#                 defaults={
#                     'id': data['id'],
#                     'name': data['name']
#                 }
#             )
#
#         if response_data_genre['next']:
#             response_data_genre = requests.get(
#                 response_data_genre['next']
#             ).json()
#         else:
#             break
#
#
#     url = 'http://warehouse:8001/warehouse/books/'
#     response_book = requests.get(url)
#     if response_book.status_code != 200:
#         return
#     response_data_book = response_book.json()
#     while 1:
#         for counter, data in enumerate(response_data_book['results']):
#             book, created = Book.objects.get_or_create(
#                 id=data['id'],
#                 defaults={
#                     'id': data['id'],
#                     "title": data['title'],
#                     "description": data['description'],
#                     "image": data['image'],
#                     "language": data['language'],
#                     "price": data['price'],
#                     "isbn": data['isbn'],
#                     "pages": data['pages'],
#                     "created": data['created'],
#                     "available": data['available'],
#                     "quantity": data['quantity'],
#                     "genre": Genre.objects.get(id=data['genre'])
#                 }
#             )
#
#             if not created:
#                 book.title = data['title']
#                 book.description = data['description']
#                 book.image = data['image']
#                 book.language = data['language']
#                 book.price = data['price']
#                 book.isbn = data['isbn']
#                 book.pages = data['pages']
#                 book.created = data['created']
#                 book.available = data['available']
#                 book.quantity = data['quantity']
#                 book.genre = Genre.objects.get(id=data['genre'])
#                 book.save()
#
#             for i in data['author']:
#                 author = Author.objects.get(id=i)
#                 book.author.add(author)
#
#         if response_data_book['next']:
#             response_data_book = requests.get(response_data_book['next']).json()
#         else:
#             break
#         print('Sync is done')
#

@shared_task
def shop_sync():
    url = 'http://warehouse:8001/warehouse/books/'
    response = requests.get(url=url).json()

    for counter, book in enumerate(response):
        if Book.objects.filter(id=book['id']).exists():
            continue
        else:
            author_list = []

            for author_resp in book['author']:
                author, created = Author.objects.get_or_create(name=author_resp['first_name', 'last_name'])
                author_list.append(author.id)

            book = Book(
                id=book['id'],
                title=book['title'],
                description=book['description'],
                image=book['image'],
                language=book['language'],
                status=book['status'],
                price=book['price'],
                isbn=book['isbn'],
                pages=book['pages'],
                created=book['created'],
                available=book['available'],
                quantity=book['quantity'],
            )
            book.save()
            for author in author_list:
                book.author.add(author)
                book.save()

    print('Sync is done')
