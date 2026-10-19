from rest_framework import generics, permissions

from apps.users.models import CustomUser
from users.serializers import (
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    pass


class LogoutView(generics.GenericAPIView):
    pass


class RefreshTokenView(generics.GenericAPIView):
    pass


class ChangePasswordView(generics.GenericAPIView):
    pass


class ForgotPasswordView(generics.GenericAPIView):
    pass


class ResetPasswordView(generics.GenericAPIView):
    pass


class UserMeView(generics.RetrieveUpdateAPIView):
    """PATCH/GET /api/users/me/"""
    
    def get_object(self):
        return self.request.user
