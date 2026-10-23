from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core import signing
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from apps.users.models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['email'],
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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        
        if not user.is_active:
            raise serializers.ValidationError('This user account is disabled.')
        
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user, context=self.context).data,
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.refresh_token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.refresh_token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError({'refresh': 'Token invalid or already expired.'})


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Recebe o e-mail do usuário e dispara o fluxo de reset.
    Retorna sempre a mesma resposta genérica para evitar enumeração de contas
    (user enumeration attack).
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        # Normaliza mas NÃO levanta erro se o e-mail não existir — proteção
        # contra enumeração de usuários (RFC 6749 / OWASP best practice).
        return value.lower().strip()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Recebe uid (base64 do UUID do usuário), token HMAC assinado e a nova senha.
    Valida integridade e expiração antes de alterar a senha.
    """
    uid   = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        uid_str   = attrs.get('uid')
        token_str = attrs.get('token')

        # 1. Decodifica o uid e localiza o usuário
        try:
            user_pk = force_str(urlsafe_base64_decode(uid_str))
            user    = CustomUser.objects.get(pk=user_pk)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError({'uid': 'Link de redefinição inválido.'})

        # 2. Valida o token HMAC com expiração via django.core.signing
        #    O salt inclui o hash atual da senha — ao redefinir a senha o token
        #    se torna automaticamente inválido (uso único garantido).
        signer = signing.TimestampSigner(salt=f'password-reset:{user.password}')
        try:
            signer.unsign(token_str, max_age=3600)  # expira em 1 hora
        except signing.SignatureExpired:
            raise serializers.ValidationError({'token': 'O link de redefinição expirou. Solicite um novo.'})
        except signing.BadSignature:
            raise serializers.ValidationError({'token': 'Token inválido ou adulterado.'})

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password', 'updated_at'])
        return user
