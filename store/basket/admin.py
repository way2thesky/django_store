# from django.contrib import admin
#
# from orders.models import Order, OrderItem
#
#
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     raw_id_fields = ['book']
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'first_name', 'last_name', 'email', 'phone_number',
#                     'address', 'postal_code', 'city', 'status',
#                     'created']
#     list_filter = ['created']
#     inlines = [OrderItemInline]
