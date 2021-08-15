from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=False, blank=False)
    profile_picture = models.ImageField(upload_to='uploads/profile_pictures', null=True, default='uploads/profile_pictures/default.png')

    def __unicode__(self):
        return self.user.username

class Post(models.Model):
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)