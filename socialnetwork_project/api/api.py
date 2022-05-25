from .serializers import *
from rest_framework import generics
from socialnetwork.models import UserProfile
from rest_framework.permissions import IsAdminUser


class UserList(generics.ListAPIView):
    """
    GET request
    returns all users
    """
    queryset = User.objects.all().distinct()
    serializer_class = UserSerializer


class UserProfileDetails(generics.RetrieveAPIView):
    """
    GET request
    receives user as parameter
    returns user profile data 
    """

    lookup_field = 'user__username'
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CreateUserProfile(generics.CreateAPIView):
    """
    Post request
    Creates new user profile
    """

    serializer_class = UserProfileSerializer


class UserPostsList(generics.ListAPIView):
    """
    GET request
    returns all posts from an user
    """
    queryset = Post.objects.all().distinct()
    serializer_class = PostSerializer

    """
    Filter the list of posts of a given author
    """
    def filter_queryset(self, queryset):
        return queryset.filter(author__username=self.kwargs.get('user__username'))


class UserFriendsDetails(generics.RetrieveAPIView):
    """
    GET request
    receives user as parameter
    returns user's friends list
    """
    lookup_field = 'user__username'
    queryset = UserProfile.objects.all()
    serializer_class = FriendSerializer


