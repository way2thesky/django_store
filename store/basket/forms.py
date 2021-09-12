from django import forms

from shop.models import Product


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    book = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())
