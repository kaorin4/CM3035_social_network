from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

# def index(request):
#     return render(request, 'socialnetwork/signup.html')

# class Index(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'socialnetwork/signup.html')

@login_required
def home(request):
    return render(request, 'socialnetwork/home.html')

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
            user_form = UserForm(data=request.POST)
            profile_form = UserProfileForm(data=request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                user = user_form.save()
                # user.set_password(user.password1)
                # user.save()
                profile = profile_form.save(commit=False)
                profile.user = user

                if 'birthday' in user_form.cleaned_data:
                    profile.birthday = request.DATA['birthday']

                profile.save()
                registered = True
                messages.success(request, 'Account created.')

                return redirect('/login')

            else:
                print(user_form.errors, profile_form.errors)
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered
        }

        return render(request, 'socialnetwork/signup.html', context)