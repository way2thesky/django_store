from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from basket.basket import Basket
from basket.forms import BasketAddBookForm
from .forms import RegisterForm
from .models import Genre, Book

User = get_user_model()


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("shop:book_list")

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


def book_list(request, genre_slug=None):
    genre = None
    genres = Genre.objects.all()

    books = Book.objects.filter(available=True)

    if genre_slug:
        genre = get_object_or_404(Genre, slug=genre_slug)
        books = books.filter(genre=genre)
    return render(request,
                  'shop/book_list.html',
                  {'genre': genre,
                   'genres': genres,
                   'books': books})


def book_detail(request, id, slug):
    basket = Basket(request)
    books = Book.objects.all()

    total_books = books.count()

    book = get_object_or_404(Book,
                             id=id,
                             slug=slug,
                             available=True)
    if request.method == "POST":
        basket_book_form = BasketAddBookForm(data=request.POST, product=book, cart=basket)
        if basket_book_form.is_valid():
            item = basket_book_form.cleaned_data
            basket.add(book=book,
                       quantity=item['quantity'],
                       override_quantity=item['override'])
            return redirect('basket:basket_detail')
    else:
        basket_book_form = BasketAddBookForm(product=book, cart=basket)

    return render(request,
                  'shop/book_detail.html',
                  {'book': book,
                   'basket_book_form': basket_book_form,
                   'total_books': total_books})
