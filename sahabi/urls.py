from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/trainer/', include('trainer_auth.urls')),
    path('api/trainee/', include('client_auth.urls')),
    path('api/tests/', include('tests.urls')),
    path('api/exercises/', include('exercise.urls')),
    path("api/analytics/", include("analytics.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
