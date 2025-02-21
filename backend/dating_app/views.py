from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes  
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from dating_app.models import User, Profile, Match, Message
from dating_app.serializers import (
    UserProfileSerializer, UserSerializer, ProfileSerializer, 
    MatchSerializer, MessageSerializer
)
from dating_app.services.matching import find_best_matches

# User-facing GUI view: renders the home page
def home_view(request):
    context = {"welcome_message": "Welcome to our Dating App!"}
    return render(request, 'dating_app/home.html', context)

# Profile API ViewSet
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return self.queryset.filter(user__id=user_id)
        return self.queryset

# View to Handle Registration
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User registered successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User API ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Match Pagination
class MatchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

# Match API ViewSet
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.select_related('user1', 'user2').all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MatchPagination

# Message API ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender', 'receiver').all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

# API to Get Current Authenticated User and Profile
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    user_serializer = UserSerializer(user)
    profile_serializer = ProfileSerializer(profile)
    return Response({
        "user": user_serializer.data,
        "profile": profile_serializer.data
    })

# API to Fetch User Matches
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_matches(request):
    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    matches = find_best_matches(user_profile)
    if not matches:
        return Response({"message": "No compatible matches found"}, status=status.HTTP_200_OK)
    return Response({
        'matches': [{'id': m['user'].id, 'username': m['user'].username, 'score': m['score']} for m in matches]
    })
