from basket.basket import Basket
from basket.forms import BasketAddBookForm

import braintree

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import BadHeaderError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.cache import cache_page   # NOQA
from django.utils.decorators import method_decorator   # NOQA

from orders.models import Order

from .forms import ContactForm, RegisterForm
from .models import Author, Book, Genre

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

User = get_user_model()


def index(request):
    return render(request, 'index.html')


# ------------------------Register----------------------------#

def signin(request):
    if request.user.is_authenticated:
        return redirect('shop:book_list')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('shop:book_list')
            else:
                messages.error(request, 'username and password doesn\'t match')

    return render(request, "registration/login.html")


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


# ------------------------Book Page----------------------------#
@method_decorator(cache_page(20), name='dispatch')
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
            basket.add(book=book)
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


# ------------------------Author Page----------------------------#
@method_decorator(cache_page(20), name='dispatch')
class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'shop/author_detail_page.html'
    slug_url_kwarg = 'author_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# ------------------------Contact US + About----------------------------#
def about(request):
    return render(request, "shop/about.html")


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


# ------------------------Search----------------------------#
@method_decorator(cache_page(20), name='dispatch')
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


# ------------------------Payment----------------------------#

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('shop:done')
        else:
            return redirect('shop:canceled')
    else:
        client_token = gateway.client_token.generate()

        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
