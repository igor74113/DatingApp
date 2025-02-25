from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi
from dating_app.views import (
    login_redirect_view, register_user, UserViewSet, ProfileViewSet, MatchViewSet, MessageViewSet, 
    current_user, get_user_matches, home_view, recommendations_view, edit_profile_view
)

# 🚀 Define API Router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'messages', MessageViewSet)

# 📜 API Documentation
swagger_schema_view = yasg_schema_view(
    openapi.Info(
        title="Django API",
        default_version='v1',
        description="API for matchmaking app",
    ),
    public=True
)

# 🌐 URL Patterns
urlpatterns = [
    # User-facing GUI pages
    path("accounts/profile/", login_redirect_view, name="login-redirect"),  # Custom login redirect
    path('', home_view, name='home'),
    path('recommendations/', recommendations_view, name='recommendations'),
    path('profile/edit/', edit_profile_view, name='edit-profile'),

    # Authentication
    path('admin/', admin.site.urls),
    path('register/', register_user, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),

    # API Endpoints
    path('api/', include(router.urls)),
    path('api/user-matches/', get_user_matches, name='get-matches'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/current-user/', current_user, name='current-user'),

    # API Documentation
    path('api/schema/', get_schema_view(title="Django API", description="API documentation", version="1.0.0"), name='openapi-schema'),
    path('api/docs/', swagger_schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]

# 📂 Serve Static Files in Debug Mode
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
