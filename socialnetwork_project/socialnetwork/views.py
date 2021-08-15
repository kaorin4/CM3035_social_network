from django.forms.models import construct_instance
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.edit import UpdateView
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

# Create your views here.

# @login_required
# def home(request):
#     return render(request, 'socialnetwork/home.html')

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
                # user.set_password(user.password1)
                # user.save()
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
        posts = Post.objects.all().order_by('-created_date')
        post_form = PostForm()

        context = {
            'post_list': posts,
            'post_form': post_form
        }

        return render(request, 'socialnetwork/home.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_date')
        post_form = PostForm(request.POST)

        if request.user.is_authenticated & post_form.is_valid():
            new_post = post_form.save(commit=False)
            # user = User.objects.get(id=user_id)
            user = User.objects.get(username=request.user.username)
            new_post.author = user 
            new_post.save()

            messages.success(request, 'Post created.')

            context = {
                'post_list': posts,
                'post_form': post_form
            }

            return render(request, 'socialnetwork/home.html', context)

class UserProfileView(View):
    def get(self, request, username, *args, **kwargs):
        profile = UserProfile.objects.get(user__username=username)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_date')

        context = {
            'user': user,
            'profile': profile,
            'post_list': posts,
        }

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

