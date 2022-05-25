from django.contrib.auth.models import User
from socialnetwork.models import UserProfile
from api.model_factories import UserFactory, UserProfileFactory
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
import json

# Create your tests here.

class GetUserTest(APITestCase):
    """
    Test module for /profile/<username> GET request
    """

    user1 = None
    good_url = ''
    bad_url = ''

    def setUp(self):
        # Create user
        self.user1 = UserProfileFactory.create()

        # Set urls
        self.good_url = reverse('api:profile_api', kwargs={'user__username': self.user1.user.username})

    def tearDown(self):

        # Reset test tables
        UserProfile.objects.all().delete()
        User.objects.all().delete()

    def test_userprofile_return_success(self):
        """
        Ensure we get an 200 OK status code when making a valid GET request to profile/<str:user__username>.
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_userprofile_return_correct_data(self):
        """
        Ensure we get the birthdate of the requested user
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        data = json.loads(response.content)
        self.assertIn(data['birthdate'], self.user1.birthdate)


class GetAllUsersTest(APITestCase):
    """
    Test module for /profiles GET request
    """

    user1 = None
    user2 = None
    good_url = ''
    bad_url = ''

    def setUp(self):
        # Create user
        self.userprofile1 = UserProfileFactory.create()
        self.user2 = UserFactory.create(username='test2', first_name='test2', last_name='test2')
        self.userprofile2 =  UserProfileFactory.create(user=self.user2, birthdate='2010-10-10')

        # Set urls
        self.good_url = reverse('api:profile_list_api')

    def tearDown(self):

        # Reset test tables
        UserProfile.objects.all().delete()
        User.objects.all().delete()

    def test_userprofiles_return_success(self):
        """
        Ensure we get an 200 OK status code when making a valid GET request to /profiles
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_userprofiles_return_correct_data(self):
        """
        Ensure we get the correct number of users
        """
        response = self.client.get(self.good_url, format='json')
        response.render()
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)


