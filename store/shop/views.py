import difflib
import functools

from django.contrib.admin.templatetags.admin_list import results
from django.contrib.auth import authenticate, login, get_user_model
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, Http404, BadHeaderError
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.views.generic import ListView, TemplateView

from basket.basket import Basket
from basket.forms import BasketAddBookForm
from .forms import RegisterForm, ContactForm
from .models import Genre, Book, Author, Slider

User = get_user_model()

class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

def about(request):
    return render(request, "shop/about.html")


def index(request):
    new_published = Book.objects.order_by('-created')[:15]
    slide = Slider.objects.order_by('-created')[:3]

    context = {
        "new_books": new_published,
        "slide": slide,
    }
    return render(request, 'index.html', context)


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


def book_detail(request, book_slug):
    basket = Basket(request)
    books = Book.objects.all()
    total_books = books.count()
    authors = Author.objects.all()
    genres = Genre.objects.all()
    book = get_object_or_404(Book,
                             slug=book_slug,
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
                   'total_books': total_books,
                   'authors': authors,
                   'genres': genres})


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'shop/author_detail_page.html'
    slug_url_kwarg = 'author_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def contact(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
                messages.add_message(request, messages.SUCCESS, 'Message sent')
            except BadHeaderError:
                messages.add_message(request, messages.ERROR, 'Message not sent')
            return redirect('/')
    return render(
        request,
        "shop/contact.html",
        context={
            "form": form,
        }
    )


def search(request):
    search = request.GET.get('q')
    books = Book.objects.all()
    if search:
        books = books.filter(
            Q(title__icontains=search) | Q(genre__name__icontains=search) | Q(author__first_name__icontains=search)

        )

    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    books = paginator.get_page(page)

    context = {
        "book": books,
        "search": search,
    }
    return render(request, 'shop/search.html', context)

