from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

def unauthenticated_user(view_funct):
    def wrapper_funct(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_funct(request, *args, **kwargs)
    return wrapper_funct


def login_required_custom(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# def allowed_users(allowed_roles=[]):
#     def decorator(view_funct):
#         def wrapper_funct(request, *args, **kwargs):
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name
#             if group in allowed_roles:
#                 return view_funct(request, *args, **kwargs)
#             else:
#                 return HttpResponse('You are not authorized to view this page.')
#         return wrapper_funct
#     return decorator

def admin_only(view_funct):
    def wrapper_funct(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'admin':
                return view_funct(request, *args, **kwargs)
            if group == 'farmers':
                return redirect('main')
            
    return wrapper_funct