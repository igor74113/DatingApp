from django import forms
from django.contrib.auth.forms import UserCreationForm
from dating_app.models import User, Profile  # Import both User & Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Enter your email"}))  

    class Meta:
        model = User  # Use custom User model
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        """Normalize email to lowercase to avoid duplicate registrations."""
        email = self.cleaned_data.get("email").lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "age", "gender", "location",
            "age_preference_min", "age_preference_max", "gender_preference",
            "diet", "exercise_routine", "sleep_schedule", "lifestyle_goal"
        ]

        widgets = {
            "age": forms.NumberInput(attrs={"min": 18, "max": 99, "placeholder": "Enter your age"}),
            "age_preference_min": forms.NumberInput(attrs={"min": 18, "max": 99, "placeholder": "Minimum age preference"}),
            "age_preference_max": forms.NumberInput(attrs={"min": 18, "max": 99, "placeholder": "Maximum age preference"}),
            "gender": forms.Select(choices=Profile._meta.get_field("gender").choices),
            "gender_preference": forms.Select(choices=Profile._meta.get_field("gender_preference").choices),
            "location": forms.TextInput(attrs={"placeholder": "Enter your city"}),
            "diet": forms.Select(choices=Profile._meta.get_field("diet").choices),
            "exercise_routine": forms.Select(choices=Profile._meta.get_field("exercise_routine").choices),
            "sleep_schedule": forms.Select(choices=Profile._meta.get_field("sleep_schedule").choices),
            "lifestyle_goal": forms.Select(choices=Profile._meta.get_field("lifestyle_goal").choices),
        }

    def clean(self):
        """Ensure required fields are filled correctly."""
        cleaned_data = super().clean()
        required_fields = [
            "age", "gender", "location",
            "age_preference_min", "age_preference_max", "gender_preference",
            "diet", "exercise_routine", "sleep_schedule", "lifestyle_goal"
        ]
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, "This field is required.")

        # Ensure age preferences make sense
        min_age = cleaned_data.get("age_preference_min")
        max_age = cleaned_data.get("age_preference_max")

        if min_age and max_age and min_age > max_age:
            self.add_error("age_preference_min", "Minimum age must be less than or equal to maximum age.")
        
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ["diet", "exercise_routine", "sleep_schedule", "lifestyle_goal"]
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, "This field is required.")
