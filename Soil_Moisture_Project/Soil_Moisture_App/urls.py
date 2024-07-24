from django.urls import path

from . import views



urlpatterns = [
     
        path('', views.landing_page, name='landing_page'),
        path('register', views.register, name='register'),
        path('login/', views.login, name='login'),
        path('logout/', views.logout, name='logout'),
        path('home/', views.home, name='home'),
        path('main/', views.main, name='main'),
        path('predict/', views.predict, name='predict'),

        
   ]