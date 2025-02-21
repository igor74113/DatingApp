from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dating_app.views import (
    register_user, UserViewSet, ProfileViewSet, MatchViewSet, MessageViewSet, 
    current_user, get_user_matches, home_view
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'messages', MessageViewSet)

swagger_schema_view = get_schema_view(
    openapi.Info(
        title="Django API",
        default_version='v1',
        description="API for matchmaking app",
    ),
    public=True
)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('register/', register_user, name='register'),

    path('accounts/', include('django.contrib.auth.urls')),  # ✅ Adds login/logout

    path('api/', include(router.urls)),
    path('api/user-matches/', get_user_matches, name='get-matches'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/current-user/', current_user, name='current-user'),
    path('api/docs/', swagger_schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]
