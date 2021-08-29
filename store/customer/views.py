from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def account_register(request):
    if request.user.is_authenticated:
        return redirect('shop:index')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = True
            user.save()

            if user is not None:
                auth.login(request, user)
                return redirect('shop:index')
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm})
