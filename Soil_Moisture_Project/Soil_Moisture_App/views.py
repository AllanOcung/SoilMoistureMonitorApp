
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth.models import Group

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import *


@unauthenticated_user
def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='farmers')

            user.groups.add(group)
            
            messages.success(request, f'Registration successful! { username }, welcome to our community.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'soil_moisture/register.html', {'form': form})


@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Implement authentication logic here
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username OR password is incorrect')

    return render(request, 'soil_moisture/login.html') 

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='login')  # This decorator makes sure the user is logged in before accessing the home page
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    return render(request, 'soil_moisture/home.html')


def Dashboard(request):
    return render(request, 'soil_moisture/Dashboard.html')