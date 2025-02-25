from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes  
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from dating_app.models import User, Profile, Match, Message  
from dating_app.serializers import (
    UserProfileSerializer, UserSerializer, ProfileSerializer,  
    MatchSerializer, MessageSerializer
)
from dating_app.services.matching import find_best_matches
from dating_app.forms import ProfileForm, CustomUserCreationForm


# Home View
def home_view(request):
    return render(request, 'dating_app/home.html', {"welcome_message": "Welcome to our Dating App!"})


# User Registration View
@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login user after registration
            return redirect("recommendations")  # Redirect to recommendations page

        return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

    form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# User API ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


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


# Get Current Authenticated User
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


# Recommendations View
@login_required
def recommendations_view(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    # Print profile fields for debugging
    print("DEBUG: Profile Fields -", {
        "age": user_profile.age,
        "gender": user_profile.gender,
        "location": user_profile.location,
        "diet": user_profile.diet,
        "exercise_routine": user_profile.exercise_routine,
        "sleep_schedule": user_profile.sleep_schedule,
        "lifestyle_goal": user_profile.lifestyle_goal,
    })

    required_fields = [
        user_profile.age, user_profile.gender, user_profile.location,
        user_profile.diet, user_profile.exercise_routine, user_profile.sleep_schedule, user_profile.lifestyle_goal
    ]
    
    if any(field is None or field == "" for field in required_fields):
        print("DEBUG: Incomplete Profile Detected. Redirecting to edit-profile.")
        return redirect("edit-profile")

    matches = find_best_matches(request.user)

    return render(request, 'dating_app/recommendations.html', {
        "user": request.user,
        "matches": [{"username": m["user"].username, "score": m["score"]} for m in matches] if matches else []
    })

# Get User Matches API
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


# Edit Profile View
@login_required
def edit_profile_view(request):
    user_profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print("DEBUG: Form Data -", cleaned_data)  # Print submitted form data
            
            # Ensure all fields are filled before saving
            if not all(cleaned_data.values()):
                form.add_error(None, "All fields are required.")
            else:
                form.save()
                print("DEBUG: Profile saved successfully.")  # Confirm save
                return redirect("recommendations")  # Redirect to recommendations

    else:
        form = ProfileForm(instance=user_profile)

    return render(request, "dating_app/edit_profile.html", {"form": form})

@login_required
def login_redirect_view(request):
    """Redirect users after login based on profile completion."""
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    # Check if profile is complete (modify conditions based on required fields)
    required_fields = [
        user_profile.age, user_profile.gender, user_profile.location,
        user_profile.diet, user_profile.exercise_routine, user_profile.sleep_schedule, user_profile.lifestyle_goal
    ]
    
    if any(field is None or field == "" for field in required_fields):  # Check for missing values
        return redirect("edit-profile")  # Redirect to profile editing page
    
    return redirect("recommendations")  # Redirect to recommendations if profile is complete
