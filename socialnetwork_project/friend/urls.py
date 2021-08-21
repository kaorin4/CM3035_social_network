from django.urls import path
from . import views

app_name = 'friend'

urlpatterns = [
    path('send_friend_request/', views.send_friend_request, name = 'send_friend_request'),
    path('accept_friend_request/', views.accept_friend_request, name = 'accept_friend_request'),
    path('decline_friend_request/', views.decline_friend_request, name = 'decline_friend_request'),
    path('cancel_friend_request/', views.cancel_friend_request, name = 'cancel_friend_request'),
    path('friend_request_list/', views.friend_request_list, name = 'friend_request_list'),
]