
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

from django.contrib.auth.models import User

import json
from django.utils import timezone

# API
import requests
from django.conf import settings

from django.shortcuts import render
import joblib
import pandas as pd



# Create your Views here:

@login_required_custom
def landing_page(request):
    return render(request, 'soil_moisture/landing_page.html')



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


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Implement authentication logic here
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.groups.filter(name='admin').exists():
                return redirect('home')
            elif user.groups.filter(name='farmers').exists():
                return redirect('main')
        else:
            messages.info(request, 'username OR password is incorrect')

    return render(request, 'soil_moisture/login.html') 

def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required_custom
def home(request):
    # Fetch Users
    users = User.objects.all()

    dashboard_context = get_dashboard_data()

    city = 'Kampala'
    weather_data = get_weather_forecast(city)

    context = {
        'users': users,
        **dashboard_context, 
        'weather_data': weather_data,
    }
    return render(request, 'soil_moisture/admin/home.html', context)

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

    # Fetch data
    data = SoilData.objects.all().values('date', 'time', 'soil_moisture', 'temperature', 'humidity')

    # Convert data to a format suitable for the frontend
    dates = [f"{item['date']}" for item in data]
    moisture_levels = [item['soil_moisture'] for item in data]
    temperature = [item['temperature'] for item in data]
    humidity = [item['humidity'] for item in data]

    # Convert data to json format
    data_json = json.dumps(list(data), default=str)

    # For Historical Data
    history = SoilData.objects.all().order_by('-date')

    dashboard_context = get_dashboard_data()

    city = 'Kampala'
    weather_data = get_weather_forecast(city)

    context = {
        'dates': json.dumps(dates),
        'moisture_levels': json.dumps(moisture_levels),
        'temperature': json.dumps(temperature),
        'humidity': json.dumps(humidity),
        'data': data_json,
        'history': history,
        **dashboard_context,   
        'weather_data': weather_data
    }

    return render(request, 'soil_moisture/user/main.html', context)



# API
def get_weather_forecast(city):
    api_key = settings.WEATHER_API_KEY
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # or 'imperial' for Fahrenheit
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

# Machine Learning Model
@login_required_custom
def predict(request):
    if request.method == 'POST':
        # Get data from the form
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        temperature = float(request.POST.get('temperature'))
        humidity = float(request.POST.get('humidity'))
        soil_texture = request.POST.get('soil_texture')
        rainfall = float(request.POST.get('rainfall'))
        
        

        # Load the model and scaler
        model = joblib.load(r'C:\Users\CISSYLINE\Desktop\Training\random_forest_model.pkl')
        scaler = joblib.load(r'C:\Users\CISSYLINE\Desktop\Training\randomScaler.pkl')

        # Prepare the data for prediction
        new_data = pd.DataFrame({
            'temperature': [temperature],
            'humidity': [humidity]
        })
        new_data_scaled = scaler.transform(new_data)

        # Make prediction
        prediction = model.predict(new_data_scaled)[0]
        prediction = round(prediction, 4)

        # Determine the comment based on the predicted soil moisture
        if prediction < 0.3:
            comment = 'Soil  dry'
        elif 0.3<= prediction <= 0.35:
            comment = 'Soil moisture moderate'
        else:
            comment = 'Soil wet'

        # Save prediction and comment to the database
        SoilData.objects.create(
            date=date,
            time=time,
            location=location,
            temperature=temperature,
            humidity=humidity,
            soil_texture=soil_texture,
            rainfall=rainfall,
            soil_moisture=prediction,
            comment=comment  
        )

        # Return the prediction and comment
        return render(request, 'soil_moisture/result.html', {'prediction': prediction, 'comment': comment})

    else:
     return render(request, 'soil_moisture/predict.html')
  

