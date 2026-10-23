from django.urls import path

from apps.users.views import (
    RegisterView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    UserMeView,
    UserImageUpdateView,
    ResetPasswordRequestView,
    ResetPasswordConfirmView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh-token'),
    path('me/', UserMeView.as_view(), name='me'),
    path('image/', UserImageUpdateView.as_view(), name='user-image-update'),
    path('password-reset/', ResetPasswordRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', ResetPasswordConfirmView.as_view(), name='password-reset-confirm'),
]
