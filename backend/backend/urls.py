# urls.py maps URLs to views acting directing HTTP requests to the appropriate view function or class.

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dating_app.views import UserViewSet, ProfileViewSet, MatchViewSet, MessageViewSet, current_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse

# router definition to the top
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'messages', MessageViewSet)

# simple root route
def root_view(request):
    return JsonResponse({"message": "Welcome to the Django API!", "endpoints": ["/api/", "/admin/"]})

urlpatterns = [
    path('', root_view, name='root'),  # default API welcome page
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/current-user/', current_user, name='current_user'),
]
