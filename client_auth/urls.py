# from django.urls import path
# from .views import SignupView, LoginView, PasswordResetRequestView, PasswordResetConfirmView

# urlpatterns = [
#     path('signup/', SignupView.as_view(), name='signup'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
#     path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
# ]
### HABIB(P):
### BALA RO DAST NAZAN BAYAD FORGOT PASSWORD RO DOROST KONAM FELA KHARABE!

from django.urls import path
from .views import TraineeDetailView, UpdateTraineeView, GetTraineeIdByUsername, GetTraineeUsernameById

urlpatterns = [
    path("info/", TraineeDetailView.as_view(), name="trainee_info"),
    path("update/", UpdateTraineeView.as_view(), name="update_trainee"),
    path('trainee-id/<str:username>/', GetTraineeIdByUsername.as_view(), name='get-trainee-id-by-username'),
    path('trainee-username/<int:trainee_id>/', GetTraineeUsernameById.as_view(), name='get-trainee-username-by-id'),
]
