from django.urls import path

from . import views



urlpatterns = [
    
        path('', views.register, name='register'),
        path('login/', views.login, name='login'),
        path('logout/', views.logout, name='logout'),
        path('home/', views.home, name='home'),
        path('main/', views.main, name='main'),
        path('trends_view/', views.trends_view, name='trends_view'),
        path('major/', views.major, name='major'),
        
   ]