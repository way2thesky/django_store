from django.urls import path, include

from . import views
from .views import Basket
from middlewares.auth import auth_middleware

app_name = 'shop'

urlpatterns = [
    path('', views.index, name="index"),
    path('shop/', views.book_list, name="book-list"),
    path('shop/<int:pk>/', views.book_detail, name="book-list"),

    # path('cart', include('django.contrib.auth.urls')),
    # https://docs.djangoproject.com/en/1.10/topics/auth/default/#module-django.contrib.auth.views

]
