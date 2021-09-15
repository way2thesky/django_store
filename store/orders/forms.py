from django import forms
from django.core.exceptions import ValidationError

from orders.models import OrderItem, Order


class OrderItemsForm(forms.ModelForm):
    def clear_quantity(self):
        data = self.cleaned_data['quantity']
        if "fred@example.com" not in data:
            raise ValidationError("You have forgotten about Fred!")

        return data

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']
