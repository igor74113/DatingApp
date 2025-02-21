from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi
from dating_app.views import (
    register_user, UserViewSet, ProfileViewSet, MatchViewSet, MessageViewSet, 
    current_user, get_user_matches, home_view
)

# Define API router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'messages', MessageViewSet)

# API Documentation
schema_view = get_schema_view(
    title="Django API",
    description="API documentation",
    version="1.0.0"
)

swagger_schema_view = yasg_schema_view(
    openapi.Info(
        title="Django API",
        default_version='v1',
        description="API for matchmaking app",
    ),
    public=True
)

urlpatterns = [
    # User-facing GUI: renders home_view (the user interface)
    path('', home_view, name='home'),
    
    # Django Admin interface
    path('admin/', admin.site.urls),
    
    # User Registration endpoint
    path('api/register/', register_user, name='register_user'),
    
    # API Endpoints from the router
    path('api/', include(router.urls)),
    
    # Custom endpoint for user matches (renamed to avoid conflict)
    path('api/user-matches/', get_user_matches, name='get-matches'),
    
    # Authentication Endpoints for JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Endpoint for fetching current authenticated user info
    path('api/current-user/', current_user, name='current-user'),
    
    # API Documentation endpoints
    path('api/schema/', schema_view, name='openapi-schema'),
    path('api/docs/', swagger_schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
