from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from Soil_Moisture_App.decorators import login_required_custom
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer


class FeedbackViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


@login_required_custom
def feedback_list(request):
    feedback = Feedback.objects.all()

    context = {
        'feedback': feedback
    }
    return render(request, 'feedback/admin-page.html', context)
