from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes  
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, Profile, Match, Message
from dating_app.serializers import UserSerializer, ProfileSerializer, MatchSerializer, MessageSerializer
from dating_app.services.matching import find_best_matches

# User API ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Profile API ViewSet
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

# Match API ViewSet
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.select_related('user1', 'user2').all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

# Message API ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender', 'receiver').all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

# API to get current authenticated user
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# API to fetch user matches
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_matches(request):
    try:
        user_profile = get_object_or_404(Profile, user=request.user)  # Ensure profile exists
    except Profile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    matches = find_best_matches(user_profile)

    if not matches:
        return Response({"message": "No compatible matches found"}, status=status.HTTP_200_OK)

    return Response({
        'matches': [{'id': m['user'].id, 'username': m['user'].username, 'score': m['score']} for m in matches]
    })
