from django import forms



class BasketAddBookForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)