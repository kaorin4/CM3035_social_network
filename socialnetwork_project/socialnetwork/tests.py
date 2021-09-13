from socialnetwork.models import UserProfile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import json

# Create your tests here.

class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', 't@t.com', 'mypassword')

    def test_login(self):
        response = self.client.post(reverse('login'), data={
            'username': 'test',
            'password': 'mypassword',
        })
        # test its redirected to home after login
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home')

class SignupTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_signup(self):
        response = self.client.post(reverse('signup'), data={
            'username': 'testuseragain',
            'email': 'another@email.com',
            'first_name': 'test 1',
            'last_name': 'test 1',
            'birthdate': '2010-12-12',
            'password1': 'stronglongpwd',
            'password2': 'stronglongpwd'
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='testuseragain')
        self.assertEqual(user.email, 'another@email.com')

class UserSearchTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', 't@t.com', 'mypassword')
        self.searched_user = User.objects.create_user('searched_test', 'st@st.com', 'smypassword')

    def test_search_user(self):
        # login
        self.client.post(reverse('login'), data={
            'username': 'test',
            'password': 'mypassword',
        })

        response = self.client.get(reverse('user-search'), {'query': 'searched_test'})
        self.assertEqual(response.status_code, 200)

class UserProfileTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', 't@t.com', 'mypassword')
        self.userprofile = UserProfile.objects.create(user=self.user, birthdate='2010-12-12')

    def test_profile_user(self):
        # login
        self.client.post(reverse('login'), data={
            'username': 'test',
            'password': 'mypassword',
        })

        # returns profile
        response = self.client.get(reverse('profile', kwargs={'username': 'test'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'socialnetwork/profile.html')

