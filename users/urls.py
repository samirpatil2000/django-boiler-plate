from django.urls import path
from users.api_views import UserRegistrationAPIView, UserProfileAPIView

urlpatterns = [
    path('', UserRegistrationAPIView.as_view(), name='register'),
    path('me/', UserProfileAPIView.as_view(), name='profile'),
]
