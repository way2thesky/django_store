from django.urls import path, include

from . import views
# from .views import Index

app_name = 'shop'

urlpatterns = [
    # path('', Index.as_view(), name="index"),
    path('', views.product_all, name="index"),
    # path('shop/<int:pk>/', views.book_detail, name="book-detail"),
    path('<slug:slug>', views.book_detail, name='book_detail'),

]
