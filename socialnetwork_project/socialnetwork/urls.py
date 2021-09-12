from django import urls
from django.urls import include, path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', login_required(login_url='/login')(views.Home.as_view()), name = 'home'),
    path('home/', login_required(login_url='/login')(views.Home.as_view()), name = 'home'),
    path('signup/', views.user_signup, name = 'signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<str:username>', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfile.as_view(), name='profile-edit'),
    path('search/', views.UserSearch.as_view(), name='user-search'),
]

# extend url patterns to include static files and images
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

