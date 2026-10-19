from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from users.models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
    
    def create(self, validated_data):
        user = CustomUser.objects._create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'image', 'is_individual', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_individual', 'created_at', 'updated_at']

