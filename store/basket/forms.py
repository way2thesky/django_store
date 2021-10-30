from django import forms


class BasketAddBookForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)

    def __init__(self, product, cart, *args, **kwargs):
        self.product = product
        self.cart = cart
        super(BasketAddBookForm, self).__init__(*args, **kwargs)

    def clean(self):
        quantity = self.cleaned_data['quantity']
        in_stock = self.cart.basket.get(str(self.product.id), {}).get("quantity", 0)
        if quantity + in_stock > self.product.quantity:
            self.add_error("quantity", "too many books: Check in Stock" )
