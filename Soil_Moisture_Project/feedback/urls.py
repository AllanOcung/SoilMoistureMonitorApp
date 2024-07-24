from django.urls import path

from .views import FeedbackViewSet, feedback_list


urlpatterns = [
    path('feedback/',
         FeedbackViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('feedback/<int:pk>/', FeedbackViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('admin/list/', feedback_list),


]
