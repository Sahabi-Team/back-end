from django.urls import path
from .views import *
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('trainers/', TrainerListCreate.as_view(), name='trainer-list'),
    path('trainers/<int:pk>/', TrainerDetail.as_view(), name='trainer-detail'),
    path('trainees/', TraineeListCreate.as_view(), name='trainee-list'),
    path('trainees/<int:pk>/', TraineeDetail.as_view(), name='trainee-detail'),
]
