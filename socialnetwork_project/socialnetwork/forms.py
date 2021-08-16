from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserSignupForm(UserCreationForm):

    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        

class UserProfileForm(forms.ModelForm):

    birthdate = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control'}))
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid': "Image files only"}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('birthdate', 'profile_picture')

class UserForm(forms.ModelForm):

    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class PostForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Whats on your mind'}))

    class Meta:
        model = Post
        fields = ['text']


