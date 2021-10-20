from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<slug:genre_slug>/', views.book_list, name='book_list_by_genre'),
    path('<int:id>/<slug:slug>/', views.book_detail, name='book_detail'),
]
