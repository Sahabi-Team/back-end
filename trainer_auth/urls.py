from django.urls import path
from .views import SignupView, LoginView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='trainer_signup'),
    path('login/', LoginView.as_view(), name='trainer_login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='trainer_password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='trainer_password_reset_confirm'),
]
