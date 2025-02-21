from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes  
from rest_framework.response import Response
from django.shortcuts import render, redirect
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from dating_app.models import Profile, Match, Message
from dating_app.serializers import (
    UserSerializer, ProfileSerializer, 
    MatchSerializer, MessageSerializer
)
from dating_app.services.matching import find_best_matches

# Get the custom User model
User = get_user_model()

# Create a custom user creation form that explicitly uses the custom user model
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User  # Explicitly set to your custom user model
        fields = ("username", "email")  # Include any additional fields if needed

# Home View (renders home page)
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
        return super().get_queryset()

# Revised User Registration View using CustomUserCreationForm
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # Redirect to login page on success
        # If form is invalid, render the template with errors
        return render(request, 'registration/register.html', {'form': form})
    
    # For GET requests, display an empty registration form
    form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

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
    
    return Response({
        "user": UserSerializer(user).data,
        "profile": ProfileSerializer(profile).data
    })

# API to Fetch User Matches
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_matches(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        matches = find_best_matches(user_profile)

        if not matches:
            return Response({"message": "No compatible matches found"}, status=status.HTTP_200_OK)

        formatted_matches = [
            {"id": match["user"].id, "username": match["user"].username, "score": match["score"]}
            for match in matches
        ]

        return Response({"matches": formatted_matches}, status=status.HTTP_200_OK)

    except Profile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
