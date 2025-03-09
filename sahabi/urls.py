from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trainer_auth.urls')),
    path('api/client_auth/', include('client_auth.urls'))
]
