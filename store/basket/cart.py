from decimal import Decimal

from django.conf import settings

from shop.models import Book


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def __iter__(self):

        book_ids = self.basket.keys()
        books = Book.objects.filter(id__in=book_ids)

        basket = self.basket.copy()
        for book in books:
            basket[str(book.id)]['book'] = book

        for pk, item in basket.items():
            item["pk"] = int(pk)
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):

        return sum(item['quantity'] for item in self.basket.values())

    def add(self, book, quantity=1, override_quantity=False):

        book_id = str(book.id)
        if book_id not in self.basket:
            self.basket[book_id] = {'quantity': 0,
                                    'price': str(book.price)}
        if override_quantity:
            self.basket[book_id]['quantity'] = quantity
        else:
            self.basket[book_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, book):

        book_id = str(book.id)
        if book_id in self.basket:
            del self.basket[book_id]
            self.save()

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())
