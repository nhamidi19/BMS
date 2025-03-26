from django.urls import path
from . import views
urlpatterns = [
    #path(<'addres':str>, <function>, <name='name':str>)
    path('', views.index, name="index"),

    #------Dist, FYI Distributions
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

    #------ Person
    #path('families/<int:family_id>/members/', views.PersonListView.as_view(), name='person_list'),  
    path('families/<int:family_id>/members/add/', views.PersonCreateView.as_view(), name='person_create'),
    path('families/<int:family_id>/members/<int:pk>/guardian/', views.set_guardian, name='person_as_guardian'),  
    path('families/<int:family_id>/members/<int:pk>/edit/', views.PersonUpdateView.as_view(), name='person_update'),  

    path('families/<int:family_id>/observations/', views.ObservationListView.as_view(), name='observation_list'),
    
]
 