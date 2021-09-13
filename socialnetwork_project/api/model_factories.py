import factory
from django.contrib.auth.models import User
from socialnetwork.models import Post, UserProfile
from django.utils.crypto import get_random_string


class UserFactory(factory.django.DjangoModelFactory):
    """Creates User test fixture"""

    username = get_random_string(length=6)
    first_name = get_random_string(length=6)
    last_name = get_random_string(length=6)

    class Meta:
        model = User

class UserProfileFactory(factory.django.DjangoModelFactory):
    """Creates UserProfile test fixture"""

    user = factory.SubFactory(UserFactory)
    birthdate = '2010-12-12'

    class Meta:
        model = UserProfile

class PostFactory(factory.django.DjangoModelFactory):
    """Creates Post test fixture"""

    text = get_random_string(length=10)

    class Meta:
        model = Post