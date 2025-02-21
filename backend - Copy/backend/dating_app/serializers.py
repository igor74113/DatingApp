from rest_framework import serializers
from dating_app.models import User, Profile, Match, Message, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

# ✅ User + Profile Combined Serializer for Registration
class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=True)
    gender = serializers.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    location = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'bio', 'profile_picture', 
                  'age', 'gender', 'location']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Handles user and profile creation"""
        profile_fields = {
            'age': validated_data.pop('age'),
            'gender': validated_data.pop('gender'),
            'location': validated_data.pop('location'),
        }

        # Create user (password hashing ensured)
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_fields)

        return user
