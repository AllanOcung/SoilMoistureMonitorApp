from django.urls import path

from . import views



urlpatterns = [
    
        path('', views.register, name='register'),
        path('login/', views.login, name='login'),
         
          #path('dashboard/', views.soil_texture_moisture_view, name='dashboard'),
        path('logout/', views.logout, name='logout'),
        path('home/', views.home, name='home'),
        path('dashboard/', views.dashboard_view, name='dashboard'),
   ]