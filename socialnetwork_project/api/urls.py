from django.urls import path
from . import api

app_name = 'api'

urlpatterns = [
    path('profiles/', api.UserList.as_view(), name='profile_list_api'),
    path('profile/<str:user__username>/', api.UserProfileDetails.as_view(), name='profile_api'),
    path('profile/', api.CreateUserProfile.as_view(), name='create_profile_api'),
    path('posts/<str:user__username>/', api.UserPostsList.as_view(), name='posts_api'),
    path('friends/<str:user__username>/', api.UserFriendsDetails.as_view(), name='friends_api'),
]