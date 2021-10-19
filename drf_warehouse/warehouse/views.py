from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.http import JsonResponse

from .models import Author, Book, Genre, Order, OrderItem
from .serializers import AuthorSerializer, BookSerializer, GenreSerializer, OrderSerializer, OrderItemSerializer, \
    GetRequestSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created')
    serializer_class = BookSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().order_by('order')
    serializer_class = OrderItemSerializer


@api_view(['POST'])
def get_request(request):
    data = JSONParser().parse(request)
    serializer = GetRequestSerializer(data=data)
    if serializer.is_valid():
        Book.objects.get(tittle=serializer.data['name']).delete()
        print('deleted')
        return JsonResponse(serializer.data, status=201)
    else:
        return JsonResponse(serializer.errors, status=400)