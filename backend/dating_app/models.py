from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    notifications_enabled = models.BooleanField(default=True)
    privacy_settings = models.JSONField(default=dict)  # Store user privacy choices

    objects = CustomUserManager()

    def __str__(self):
        return self.username

# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Basic Info
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        default='Other'
    )
    location = models.CharField(max_length=255, blank=True, null=True)

    # Age Preferences for Matching
    age_preference_min = models.IntegerField(null=True, blank=True, default=18)
    age_preference_max = models.IntegerField(null=True, blank=True, default=99)
    gender_preference = models.CharField(
        max_length=20,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'), ('Any', 'Any')],
        default='Any'
    )

    # Health and Lifestyle Fields
    diet = models.CharField(
        max_length=50, 
        choices=[('vegan', 'Vegan'), ('keto', 'Keto'), ('balanced', 'Balanced'), ('paleo', 'Paleo')],
        blank=True, null=True
    )
    exercise_routine = models.CharField(
        max_length=50, 
        choices=[('gym', 'Gym'), ('yoga', 'Yoga'), ('running', 'Running'), ('none', 'None')],
        blank=True, null=True
    )
    sleep_schedule = models.CharField(
        max_length=50, 
        choices=[('early_riser', 'Early Riser'), ('night_owl', 'Night Owl'), ('flexible', 'Flexible')],
        blank=True, null=True
    )
    lifestyle_goal = models.CharField(
        max_length=100, 
        choices=[('weight_loss', 'Weight Loss'), ('muscle_gain', 'Muscle Gain'), ('stress_management', 'Stress Management')],
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.username} Profile"

# Match Model
class Match(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matches_initiated')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matches_received')
    match_score = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match: {self.user1} & {self.user2} ({self.match_score})"

# Messages Model
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:30]}"

# Notifications Model
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

# Auto-create profile when a new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
