from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Workout API",
        default_version='v1',
        description="Workout, Exercises, and Filtering API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[], 
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/trainer/', include('trainer_auth.urls')),
    path('api/trainee/', include('client_auth.urls')),
    path('api/tests/', include('tests.urls')),
    path('api/exercises/', include('exercise.urls')),
    path("api/analytics/", include("analytics.urls")),
    path("api/workout/", include("workout.urls")),
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
