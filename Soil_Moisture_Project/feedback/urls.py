from django.urls import path

from .views import FeedbackViewSet


urlpatterns = [
    path('feedback/',
         FeedbackViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('feedback/<int:pk>/', FeedbackViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),


]
