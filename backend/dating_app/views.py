from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes  
from rest_framework.response import Response
from .models import User, Profile, Match, Message
from dating_app.serializers import UserSerializer, ProfileSerializer, MatchSerializer, MessageSerializer

# User API ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Profile API ViewSet
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

# Match API ViewSet
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

# Message API ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

# API to get current authenticated user
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])  # Now correctly imported
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
