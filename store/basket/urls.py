from django.urls import path

from . import views
from .views import CheckOut

app_name = 'basket'

urlpatterns = [
    path('basket/', views.basket_summary, name='basket_summary'),
    path('add/', views.basket_add, name='basket_add'),
    path('delete/', views.basket_delete, name='basket_delete'),
    path('update/', views.basket_update, name='basket_update'),
    path('check-out', CheckOut.as_view(), name='checkout'),

]