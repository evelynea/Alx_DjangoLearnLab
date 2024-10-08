from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField()
    bio = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'password', 
            'password2', 
            'bio', 
            'profile_picture'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 as it's not needed
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)  # Create a token for the new user
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, 
        max_length=150
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Both username and password are required.")

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'followers_count', 'following_count']