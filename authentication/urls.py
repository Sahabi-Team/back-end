from django.urls import path
from .views import LoginView, RegisterView, ChangePasswordView, PasswordResetRequestView, PasswordResetConfirmView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-password/', PasswordResetRequestView.as_view(), name='request-reset-password'),
    path('reset-password/<uid>/<token>/', PasswordResetConfirmView.as_view(), name='reset-password'),
]
