from django import urls
from django.urls import include, path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path('', views.index, name = 'index'),
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('api/protein/<str:protein_id>/', api.ProteinDetails.as_view(), name='protein_api'),
    # path('api/pfam/<str:domain_id>/', api.PfamDetails.as_view(), name='pfam_api'),
    # path('api/proteins/<str:taxa_id>/', api.FilterProteinDomainByTaxonomy.as_view(), name='protein_tax_api'),
    # path('api/pfams/<str:taxa_id>/', api.FilterDomainByTaxonomy.as_view(), name='domain_tax_api'),
    # path('api/coverage/<str:protein_id>/', api.ProteinCoverage.as_view(), name='protein_coverage'),
    # path('api/protein/', api.PostProteinDetails.as_view(), name='create_protein_api'),
]

urlpatterns += staticfiles_urlpatterns()