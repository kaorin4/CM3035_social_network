from django.contrib import auth
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from friend.helpers import find_friend_request
from friend.models import FriendRequest
from django.db.models.query_utils import Q
from django.db.models.functions import Concat 
from django.db.models import Value as V

# Create your views here.


@login_required
def user_logout(request):
    logout(request)
    return redirect('/login')

def user_login(request):

    if request.user.is_authenticated:
        return redirect('/home')
    else:

        if request.method == 'POST':

            form = AuthenticationForm(request=request, data=request.POST)

            if form.is_valid() and form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Logged in.')

                    return redirect('/home')
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid login details supplied.')

        return render(request, 'socialnetwork/login.html')


def user_signup(request):

    if request.user.is_authenticated:
        return redirect('/home')
    else:

        registered = False

        if request.method == 'POST':
            user_form = UserSignupForm(data=request.POST)
            profile_form = UserProfileForm(data=request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                user = user_form.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                if 'birthdate' in user_form.cleaned_data:
                    profile.birthdate = request.DATA['birthdate']

                profile.save()
                registered = True
                messages.success(request, 'Account created.')

                return redirect('/login')

            else:
                print(user_form.errors, profile_form.errors)
        else:
            user_form = UserSignupForm()
            profile_form = UserProfileForm()

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered
        }

        return render(request, 'socialnetwork/signup.html', context)


class Home(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.filter(user=user).first()

        if profile is not None:

            user_friends = user.userprofile.friends.all()
            feed_posts = Post.objects.filter(Q(author__in=user_friends) | Q(author=user)).order_by('-created_date')

            post_form = PostForm()

            context = {
                'post_list': feed_posts,
                'post_form': post_form
            }

            return render(request, 'socialnetwork/home.html', context)

        else:
            messages.error(request, 'Create an account.')
            logout(request)
            return redirect('/login')

    def post(self, request, *args, **kwargs):

        post_form = PostForm(request.POST, request.FILES)

        if request.user.is_authenticated & post_form.is_valid():
            new_post = post_form.save(commit=False)
            user = request.user
            new_post.author = user 

            new_post.save()

            user_friends = user.userprofile.friends.all()
            feed_posts = Post.objects.filter(Q(author__in=user_friends) | Q(author=user)).order_by('-created_date')

            messages.success(request, 'Post created.')

            new_post_form = PostForm()

            context = {
                'post_list': feed_posts,
                'post_form': new_post_form
            }

            return render(request, 'socialnetwork/home.html', context)

class UserProfileView(View):

    def get(self, request, username, *args, **kwargs):

        context = {}
        profile = UserProfile.objects.get(user__username=username)
        profile_user = profile.user
        profile_posts = Post.objects.filter(author=profile_user).order_by('-created_date')
        profile_friends = profile.friends.all()

        user = request.user

        is_logged_user = False
        is_friend = False
        if user.is_authenticated and user != profile_user:
            is_logged_user = False
            if profile_friends.filter(username=user.username):
                is_friend = True
            else: 
                is_friend = False
                # if not friends, check if there is an active friend request
                # logged user has pending request 
                if find_friend_request(user_sender=profile_user, user_receiver=user) != False:
                    friend_request_sent_to_user = find_friend_request(user_sender=profile_user, user_receiver=user)
                    pending_to_user_id = friend_request_sent_to_user.id
                    context['pending_to_user_id'] = pending_to_user_id
                    context['sent_request'] = 'sent_to_user'
                # the other user has a pending request
                elif find_friend_request(user_sender=user, user_receiver=profile_user) != False:
                    friend_request_sent_by_user = find_friend_request(user_sender=user, user_receiver=profile_user)
                    pending_to_them_id = friend_request_sent_by_user.id
                    context['pending_to_them_id'] = pending_to_them_id
                    context['sent_request'] = 'sent_to_them'
                # there are no requests
                else:
                    context['sent_request'] = 'no_request'

        elif user.is_authenticated and user == profile_user:
            is_logged_user = True
            friend_requests_received = FriendRequest.objects.filter(receiver=user, is_active=True)
            friend_requests_sent = FriendRequest.objects.filter(sender=user, is_active=True)
            context['friend_requests_received'] = friend_requests_received
            context['friend_requests_sent'] = friend_requests_sent

        context['user'] = user
        context['profile'] = profile
        context['post_list'] = profile_posts
        context['is_logged_user'] = is_logged_user
        context['is_friend'] = is_friend
        context['friends'] = profile_friends

        return render(request, 'socialnetwork/profile.html', context)


class EditProfile(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(UserProfile, user=user)

        user_form = UserSignupForm(request.POST or None,
                            request.FILES or None, 
                            instance=user)
        profile_form = UserProfileForm(request.POST or None,
                            request.FILES or None, 
                            instance=profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile
        }

        return render(request, 'socialnetwork/profile_edit.html', context)


    def post(self, request, *args, **kwargs):

        user = request.user
        profile = get_object_or_404(UserProfile, user=user)

        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile edited.')

            return redirect('/profile/'+user.username)

        else:
            print(user_form.errors, profile_form.errors)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }

        return render(request, 'socialnetwork/profile_edit.html', context)


class UserSearch(View):

    def get(self, request, *args, **kwargs):
        user_searched = self.request.GET.get('query')
        users = User.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(
            Q(username__icontains=user_searched)|
            Q(first_name__icontains=user_searched)|
            Q(last_name__icontains=user_searched)|
            Q(full_name__icontains=user_searched)
        )

        context = {
            'users': users,
        }

        return render(request, 'socialnetwork/user_search.html', context)


