from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes  
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from dating_app.models import User, Profile, Match, Message
from dating_app.serializers import UserSerializer, ProfileSerializer, MatchSerializer, MessageSerializer
from dating_app.services.matching import find_best_matches
from rest_framework.pagination import PageNumberPagination
from dating_app.models import Match
from rest_framework import viewsets

class MatchPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow clients to specify page size
    max_page_size = 50  # Limit the maximum page size

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MatchPagination 

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
class MatchPagination(PageNumberPagination):
    page_size = 10  # Number of matches per page
    page_size_query_param = 'page_size'  # Allows frontend to specify page size
    max_page_size = 50  # Prevents excessive data requests

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.select_related('user1', 'user2').all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MatchPagination  # Apply pagination here


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
