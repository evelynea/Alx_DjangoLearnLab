from django.contrib.auth import views as auth_views

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.db import models

class LoginView(auth_views.LoginView):
    template_name = 'auth/login.html'

class LogoutView(auth_views.LogoutView):
    template_name = 'auth/logged_out.html'


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2'
        ]
    
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        # Handle profile update logic here
        pass
    return render(request, 'auth/profile.html')