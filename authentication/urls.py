from django.urls import path
from .views import LoginView, RegisterView, ChangePasswordView, PasswordResetRequestView, PasswordResetConfirmView, WhoAmI, UpdateProfilePictureView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('whoami/', WhoAmI.as_view(), name='whoami'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-password/', PasswordResetRequestView.as_view(), name='request-reset-password'),
    path('reset-password/<str:token>/', PasswordResetConfirmView.as_view(), name='reset-password'),
    path('update-profile-picture/', UpdateProfilePictureView.as_view(), name='update-profile-picture'),
]
