from crispy_forms.helper import FormHelper

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from shop.models import Review

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class ReviewForm(forms.ModelForm):
    review_star = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    review_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write Your Review'}))

    class Meta:
        model = Review
        fields = [
            'review_star',
            'review_text'
        ]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
