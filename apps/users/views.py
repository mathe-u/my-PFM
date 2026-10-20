from rest_framework import generics, permissions, parsers, status
from rest_framework.response import Response

from apps.users.models import CustomUser
from users.serializers import (
    RegisterSerializer,
    LoginSetializer,
    LogoutSerializer,
    UserSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSetializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView():
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_204_NO_CONTENT)


class RefreshTokenView():
    permission_classes = [permissions.AllowAny]


class ChangePasswordView():
    pass


class ForgotPasswordView():
    pass


class ResetPasswordView():
    pass


class UserImageUpdateView():
    pass


class UserMeView(generics.RetrieveUpdateAPIView):
    """PATCH/GET /api/users/me/"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
