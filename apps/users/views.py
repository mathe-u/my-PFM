from rest_framework import generics, permissions
from apps.users.models import CustomUser


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = None
    permission_classes = [permissions.AllowAny]


class LoginView:
    pass


class LogoutView:
    pass


class RefreshTokenView:
    pass


class ChangePasswordView:
    pass


class ForgotPasswordView:
    pass


class ResetPasswordView:
    pass


class UserMeView:
    """PATCH/GET /api/users/me/"""
    pass