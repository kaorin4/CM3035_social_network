from django import urls
from django.urls import include, path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('', views.index, name = 'index'),
    # path('home/', views.home, name = 'home'),
    path('home/', login_required(login_url='/login')(views.Home.as_view()), name = 'home'),
    path('signup/', views.user_signup, name = 'signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<str:username>', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfile.as_view(), name='profile-edit'),
    # path('profile/edit/<int:pk>', views.UserProfileEditView.as_view(), name='profile-edit'),
    # path('api/protein/<str:protein_id>/', api.ProteinDetails.as_view(), name='protein_api'),
    # path('api/pfam/<str:domain_id>/', api.PfamDetails.as_view(), name='pfam_api'),
    # path('api/proteins/<str:taxa_id>/', api.FilterProteinDomainByTaxonomy.as_view(), name='protein_tax_api'),
    # path('api/pfams/<str:taxa_id>/', api.FilterDomainByTaxonomy.as_view(), name='domain_tax_api'),
    # path('api/coverage/<str:protein_id>/', api.ProteinCoverage.as_view(), name='protein_coverage'),
    # path('api/protein/', api.PostProteinDetails.as_view(), name='create_protein_api'),
]

# extend url patterns to include static files and images
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

