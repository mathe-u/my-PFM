from rest_framework import generics, permissions, parsers, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

from django.core import signing
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings

from apps.users.models import CustomUser
from apps.users.serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_204_NO_CONTENT)


class RefreshTokenView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class ChangePasswordView():
    pass


class VerifyEmailView():
    pass


class ResetPasswordRequestView(generics.GenericAPIView):
    """
    POST /api/auth/password-reset/
    Corpo: { "email": "user@example.com" }

    Gera um token HMAC assinado (TimestampSigner) com expiração de 1 hora
    e "envia" o e-mail via console backend (impresso no terminal).
    A resposta é SEMPRE a mesma, independente de o e-mail existir ou não,
    para evitar ataques de enumeração de contas (OWASP A07).
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    # URL base do front-end para compor o link (ajuste em produção via settings)
    FRONTEND_RESET_URL = getattr(settings, 'FRONTEND_RESET_PASSWORD_URL', 'http://localhost:3000/reset-password')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # Resposta genérica: não revelamos se o e-mail existe ou não
            return Response(
                {'detail': 'Se esse e-mail estiver cadastrado, você receberá as instruções em breve.'},
                status=status.HTTP_200_OK,
            )

        # --- Geração do token ---
        # uid: UUID do usuário codificado em base64 (URL-safe, sem padding `=`)
        uid = urlsafe_base64_encode(force_bytes(str(user.pk)))

        # O salt inclui o hash da senha atual: quando o usuário redefinir a senha
        # o token se torna automaticamente inválido (uso único garantido sem BD).
        signer = signing.TimestampSigner(salt=f'password-reset:{user.password}')
        token  = signer.sign(uid)  # payload: "<uid>:<timestamp>:<signature>"

        reset_link = f'{self.FRONTEND_RESET_URL}?uid={uid}&token={token}'

        # --- Simulação de envio ---
        # EMAIL_BACKEND = console.EmailBackend → imprime no terminal, não envia de verdade.
        send_mail(
            subject='[MyPFM] Redefinição de senha',
            message=(
                f'Olá, {user.name}!\n\n'
                f'Recebemos uma solicitação para redefinir a senha da sua conta.\n\n'
                f'Clique no link abaixo para criar uma nova senha (válido por 1 hora):\n'
                f'{reset_link}\n\n'
                f'Se você não solicitou isso, ignore este e-mail.\n'
                f'Sua senha permanece inalterada.'
            ),
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@mypfm.local'),
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(
            {'detail': 'Se esse e-mail estiver cadastrado, você receberá as instruções em breve.'},
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirmView(generics.GenericAPIView):
    """
    POST /api/auth/password-reset/confirm/
    Corpo: { "uid": "...", "token": "...", "new_password": "..." }

    Valida o token HMAC (integridade + expiração) e redefine a senha.
    Após o reset o token é automaticamente invalidado pois o salt muda.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': 'Senha redefinida com sucesso.'},
            status=status.HTTP_200_OK,
        )


class UserImageUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMeView(generics.RetrieveUpdateAPIView):
    """PATCH/GET /api/users/me/"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
