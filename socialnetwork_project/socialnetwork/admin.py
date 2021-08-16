from django.contrib import admin
from .models import *

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    # list_display = ('get_friends', 'user')
    search_fields = ['user']


    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post)