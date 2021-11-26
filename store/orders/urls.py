from django.urls import path


from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name="order_list"),
    path('create/', views.order_create, name='order_create'),
    path('pdf/<int:id>', views.pdf.as_view(), name="pdf"),

]
