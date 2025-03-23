from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    # path('api/trainer_auth/', include('trainer_auth.urls')),
    path('api/trainee/', include('client_auth.urls'))
]
