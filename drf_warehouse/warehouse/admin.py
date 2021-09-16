from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'created', 'status']
    list_filter = ['status']


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity', 'price']
