from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Create your views here.

# def index(request):
#     return render(request, 'socialnetwork/signup.html')

# class Index(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'socialnetwork/signup.html')

@login_required
def logout(request):
    logout(request)
    return HttpResponseRedirect('../test')

def login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                # return HttpResponseRedirect('../test')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'socialnetwork/login.html')


def signup(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'birthday' in user_form.cleaned_data:
                profile.birthday = request.DATA['birthday']

            profile.save()
            registered = True

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