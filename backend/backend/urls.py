"""
URLs file for Django API
- Maps URLs to views, handling HTTP requests
- Uses DefaultRouter for ViewSets
- Includes JWT authentication & API documentation
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi

# Import Views
from dating_app.views import (
    UserViewSet, ProfileViewSet, MatchViewSet, MessageViewSet, 
    current_user, get_user_matches
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

# Simple Root Route
def root_view(request):
    return JsonResponse({"message": "Welcome to the Django API!", "endpoints": ["/api/", "/admin/"]})

# URL Patterns
urlpatterns = [
    # General routes
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/', include(router.urls)),
    path('api/matches/', get_user_matches, name='get-matches'),
    
    # Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User-related API
    path('api/current-user/', current_user, name='current-user'),
    
    # API Documentation
    path('api/schema/', schema_view, name='openapi-schema'),
    path('api/docs/', swagger_schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]
