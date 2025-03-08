from django.urls import path
from . import views

urlpatterns = [
    path('api/trainer_signup/', views.trainer_signup, name='trainer_signup'),
    path('api/trainer_login/', views.trainer_login, name='trainer_login'),
]
