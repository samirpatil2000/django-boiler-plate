from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers.user_serializer import UserSerializer


class UserRegistrationAPIView(APIView):
    def post(self, request):
        """
        Register a new user account
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_data = {
            "email": user.email,
            "date_joined": user.date_joined
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
