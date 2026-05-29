import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.serializers.user_serializer import UserSerializer
from users.models import User


class UserProfileAPIView(APIView):
    def get_permissions(self):
        disable_auth = os.environ.get('DISABLE_AUTH', 'False').lower() == 'true'
        if disable_auth:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        """
        Get the authenticated user's profile.
        If DISABLE_AUTH is enabled and no credentials are provided,
        falls back to a default developer user.
        """
        user = request.user
        
        if not user.is_authenticated:
            # Fallback to dev user if auth is disabled and request is anonymous
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(
                    email="dev@example.com",
                    password="devpassword123"
                )
                
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
