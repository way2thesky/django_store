from django.urls import path

from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_detail, name='basket_detail'),
    path('update/<int:book_id>/', views.basket_update, name='basket_update'),
    path('summary/', views.basket_summary, name='basket_summary'),
    path('added/<int:book_id>/', views.basket_add, name='basket_add'),
    path('remove/<int:book_id>/', views.basket_remove, name='basket_remove'),
]
