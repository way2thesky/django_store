from django import forms

from orders.models import Order


class OrderItemsForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address','phone_number',
                  'postal_code', 'city']
