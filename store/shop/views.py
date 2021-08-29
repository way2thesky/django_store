
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def book_list(request):
    return render(request, 'shop/book_list.html')


def book_detail(request):
    return render(request, 'shop/book_detail.html')
