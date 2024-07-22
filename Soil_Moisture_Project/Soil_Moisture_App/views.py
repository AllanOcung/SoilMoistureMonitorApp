
from audioop import avg
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth.models import Group
from .models import SoilData
from django.db.models import Avg

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import *

import json


@unauthenticated_user
@login_required_custom
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


@login_required_custom
@admin_only
def home(request):
    return render(request, 'soil_moisture/admin/home.html')

def get_dashboard_data():
    # Fetch all entries
    entries = SoilData.objects.all()
    data = [
        {
            'date': entry.date.strftime('%Y-%m-%d'),
            'time': entry.time.strftime('%H:%M:%S'),
            'soil_moisture': round(entry.soil_moisture, 2),
            'temperature': round(entry.temperature, 2),
            'humidity': round(entry.humidity, 2),
            'rainfall': round(entry.rainfall, 2)
        }
        for entry in entries
    ]
    
    # Calculate average soil moisture per soil texture
    soil_texture_data = SoilData.objects.values('soil_texture').annotate(
        avg_moisture=Avg('soil_moisture')
    )
    
    # Calculate average rainfall per area
    average_rainfall_per_area = SoilData.objects.values('location').annotate(
        avg_rainfall=Avg('rainfall')
    )

    # Transform soil_texture_data for horizontal display
    soil_texture_headers = [item['soil_texture'] for item in soil_texture_data]
    avg_moistures = [round(item['avg_moisture'], 2) for item in soil_texture_data]

    # Calculate average soil moisture and average rainfall per location
    location_data = SoilData.objects.values('location').annotate(
        avg_moisture=Avg('soil_moisture'),
        avg_rainfall=Avg('rainfall')
    )

    # Round off the values in location_data
    location_data = [
        {
            'location': item['location'],
            'avg_moisture': round(item['avg_moisture'], 2),
            'avg_rainfall': round(item['avg_rainfall'], 2)
        }
        for item in location_data
    ]

    context = {
        'data': data,
        'soil_texture_headers': soil_texture_headers,
        'avg_moistures': avg_moistures,
        'average_rainfall_per_area': [
            {
                'location': item['location'],
                'avg_rainfall': round(item['avg_rainfall'], 2)
            }
            for item in average_rainfall_per_area
        ],
        'location_data': location_data
    }
    
    return context

@login_required_custom
def main(request):
    history = SoilData.objects.all().order_by('-date')  #[:20]

    dashboard_context = get_dashboard_data()

    data = SoilData.objects.all().values('date', 'time', 'soil_moisture', 'temperature', 'humidity')
    
    # Convert data to json format
    data_json = json.dumps(list(data), default=str)

    context = {
        'history': history,
        **dashboard_context,
        'data': data_json
    }
    return render(request, 'soil_moisture/main.html', context)



def trends_view(request):

    data = SoilData.objects.all().values('date', 'time', 'soil_moisture', 'temperature', 'humidity')

    # Convert data to json format

    data_json = json.dumps(list(data), default=str)

    return render(request, 'soil_moisture/main2.html', {'data': data_json})

def major(request):
    get = SoilData.objects.all()

    dashboard_context = get_dashboard_data()

    context = {
        'get': get,
        **dashboard_context,  # Include the dashboard data in the context for the major template.
      
        
    }

    return render(request, 'soil_moisture/major.html', context)


def dashboard(request):
    return render(request, 'soil_moisture/Dashboard.html')