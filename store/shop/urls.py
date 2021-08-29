from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name="index"),
    path('shop/', views.book_list, name="book-list"),
    path('shop/<int:pk>/', views.book_detail, name="book-list"),

]