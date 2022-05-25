from django.contrib.auth.models import User
from rest_framework import serializers
from socialnetwork.models import UserProfile, Post

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_joined')

class UserProfileSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(required=True)
    friends = UserSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'birthdate', 'profile_picture', 'friends')

    def create(self, validated_data):

        # create user 
        user = User.objects.create(
            username = validated_data['user']['username'],
            first_name = validated_data['user']['first_name'],
            last_name = validated_data['user']['last_name'],
            email = validated_data['user']['email'],
        )

        # create profile
        profile = UserProfile.objects.create(
            user = user,
            birthdate = validated_data['birthdate'],
            profile_picture = validated_data['profile_picture'],
        )

        return profile


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('text', 'image', 'created_date')


class FriendSerializer(serializers.ModelSerializer):
    
    friends = UserSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('friends',)