from decimal import Decimal

from django.conf import settings

from shop.models import Book


class Basket(object):
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, book):
        book_id = str(book.id)
        if book_id not in self.basket:
            self.basket[book_id] = {'quantity': 0, 'price': str(book.price)}
            self.basket[book_id]['quantity'] = 1
        else:
            if self.basket[book_id]['quantity'] < 1:
                self.basket[book_id]['quantity'] += 1

        self.save()

    def update(self, book, quantity):
        book_id = str(book.id)
        self.basket[book_id]['quantity'] = quantity

        self.save()

    def save(self):
        self.session[settings.BASKET_SESSION_ID] = self.basket
        self.session.modified = True

    def remove(self, book):
        book_id = str(book.id)
        if book_id in self.basket:
            del self.basket[book_id]
            self.save()

    def __iter__(self):
        book_ids = self.basket.keys()
        books = Book.objects.filter(id__in=book_ids)
        for book in books:
            self.basket[str(book.id)]['book'] = book

        for item in self.basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True
