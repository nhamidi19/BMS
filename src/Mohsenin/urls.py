from django.urls import path
from . import views
urlpatterns = [
    #path(<'addres':str>, <function>, <name='name':str>)
    path('', views.index, name="index"),

    #----- Dist, FYI Distributions
    path('dists/', views.DistListView.as_view(), name='dist_list'),
    path('dist/create/', views.DistCreateView.as_view(), name='dist_create'),
    path('dist/<int:pk>/update', views.DistUpdateView.as_view(), name='dist_update'),
    path('dist/<int:pk>/delete/', views.DistDeleteView.as_view(), name='dist_delete'),

    #----- Family
    path('families/', views.FamilyListView.as_view(), name='family_list'),  
    path('families/create/', views.FamilyCreateView.as_view(), name='family_create'),  
    path('families/<int:pk>/', views.FamilyDetailView.as_view(), name='family_detail'),  
    path('families/<int:pk>/update/', views.FamilyUpdateView.as_view(), name='family_update'),  
    path('families/<int:pk>/deactivate/', views.FamilyDeactivateView.as_view(), name='family_deactivate'),
    path("family_convert_xml", views.family_list , name="download_family"),

    #------ Person
    path('families/<int:family_id>/members/', views.PersonListView.as_view(), name='person_list'),  
    path('families/<int:family_id>/members/add/', views.PersonCreateView.as_view(), name='person_add'),  
    path('families/<int:pk>/member', views.PersonDetailView.as_view(), name='person_detail'),  
    path('families/<int:family_id>/members/<int:pk>/edit/', views.PersonUpdateView.as_view(), name='person_edit'),  
    path('families/<int:family_id>/members/<int:pk>/deactive/', views.PersonDeactivateView.as_view(), name='person_delete'),
    path("person_convert_xml/", views.person_list , name="download_person"),



    ##----- Observation
    path('families/<int:family_id>/observations/', views.ObservationListView.as_view(), name='observation_list'),
    path('families/<int:family_id>/observations/add', views.ObservationCreateView.as_view(), name='observation_create'),
    path('families/<int:family_id>/observations/<int:observation_id>/detail', views.ObservationsDetailsView.as_view(), name='observation_detail'),
    path('families/<int:family_id>/observations/<int:observation_id>/update', views.ObservationsUpdateView.as_view(), name="observation_update"),
    path('observaion_convert_xml', views.observation_list, name="download_observation"),
    

    #----- Packages
    path("packages/", views.PackageListView.as_view(), name="packages_list"),
    path("packages/add/", views.PackageCreateView.as_view(), name="package_create"),
    path("packages/<int:pk>/update/", views.PackageUpdateView.as_view(), name="package_update"),
    path("packages/<int:pk>/delete/", views.PackageDeleteView.as_view(), name="package_delete"),
    path("packages/<int:pk>/", views.PackageDetailView.as_view(), name="package_detail"),
    path("packages_convert_xml", views.package_list, name="download_package"),

    #----- Packages Distribution
    path("packages_distribution/", views.PackageDistributionListView.as_view(), name="packageshare_list"),
    path("packages_distribution/add/", views.PackageDistributionCreate.as_view(), name="packageshare_create"),
    path("packages_distribution/<int:pk>/update", views.PackageDistributionUpdate.as_view(), name="packageshare_update"),
    path("packages_distribution/<int:pk>/detail", views.PackageDistributionDetail.as_view(), name="packageshare_detail"),
    path("packages_distribution/<int:pk>/deactive/", views.PackageDistributionDeactive.as_view(), name="packageshare_deactive"),
    path("packages_distribution_convert_xml", views.packageDistribtion_list, name="download_packagedistribtion"),

    #----- Packages Distribution
    path("medicalaids/", views.MedicalAidListView.as_view(), name="medicalaid_list"),
    path("medicalaids/add", views.MedicalAidCreateView.as_view(), name="medicalaid_create"),
    path("medicalaids/<int:pk>/update", views.MedicalAidUpdateView.as_view(), name="medicalaid_update"),
    path("medicalaids/<int:pk>/detail", views.MedicalAidDetailView.as_view(), name="medicalaid_detail"),
    path("medicalaids_convert_xml", views.medicalaidlist, name="download_medicalaid"),

    #----- Packages Distribution
    path("inmaterelease/", views.InmateReleaseListView.as_view(), name="inmaterelease_list"),
    path("inmaterelease/add/", views.InmateReleaseCreateView.as_view(), name="inmaterelease_create"),
    path("inmaterelease/<int:pk_object>/update/", views.InmateReleaseUpdateView.as_view(), name="inmaterelease_update"),
    path("inmaterelease/<int:pk_object>/", views.InmateReleaseDetail.as_view(), name="inmaterelease_detail"),
    path("inmaterelease_convert_xml", views.inmaterelease_list, name="download_inmaterelease"),

]
 