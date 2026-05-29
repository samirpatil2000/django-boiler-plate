from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')

        # Check if email is already taken
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})

        # Check if passwords match
        if password != password2:
            raise serializers.ValidationError({'password': 'Password mismatch'})

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
