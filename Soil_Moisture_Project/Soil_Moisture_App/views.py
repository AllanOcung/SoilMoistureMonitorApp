
from audioop import avg
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib import messages
from django.shortcuts import render
from .models import SoilData
from django.db.models import Avg


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')

            messages.success(request, f'Registration successful! { user}, welcome to our community.')
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
            return redirect('home')
        else:
            return render(request, 'soil_moisture/login.html', {
                'message': 'Invalid username or password'
                })

    return render(request, 'soil_moisture/login.html') 

def home(request):
    return render(request, 'soil_moisture/home.html')
# what i added

def dashboard_view(request):
    # Fetch all entries
    entries = SoilData.objects.all()
    data = [
        {
            'date': entry.date.strftime('%Y-%m-%d'),
            'time': entry.time.strftime('%H:%M:%S'),
            'soil_moisture': entry.soil_moisture,
            'temperature': entry.temperature,
            'humidity': entry.humidity,
            'rainfall': entry.rainfall
        }
        for entry in entries
    ]
    
    # Calculate average soil moisture per soil texture
    soil_texture_data = SoilData.objects.values('soil_texture').annotate(avg_moisture=Avg('soil_moisture'))
    
    # Calculate average rainfall per area
    average_rainfall_per_area = SoilData.objects.values('location').annotate(avg_rainfall=Avg('rainfall'))

    # Transform soil_texture_data for horizontal display
    soil_texture_headers = [item['soil_texture'] for item in soil_texture_data]
    avg_moistures = [item['avg_moisture'] for item in soil_texture_data]
     # Calculate average soil moisture and average rainfall per location
    location_data = SoilData.objects.values('location').annotate(
        avg_moisture=Avg('soil_moisture'),
        avg_rainfall=Avg('rainfall')
    )

    context = {
        'data': data,
        'soil_texture_headers': soil_texture_headers,
        'avg_moistures': avg_moistures,
        'average_rainfall_per_area': list(average_rainfall_per_area),
        'location_data': location_data
    }
    
    return render(request, 'soil_moisture/Dashboard.html', context)