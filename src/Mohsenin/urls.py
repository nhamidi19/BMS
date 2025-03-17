from django.urls import path
from . import views
urlpatterns = [
    #path(<'addres':str>, <function>, <name='name':str>)
    path('', views.index, name="index"),
    path('families/', views.FamilyListView.as_view(), name='family_list'),  
    path('families/create/', views.FamilyCreateView.as_view(), name='family_create'),  
    path('families/<int:pk>/', views.FamilyDetailView.as_view(), name='family_detail'),  
    path('families/<int:pk>/update/', views.FamilyUpdateView.as_view(), name='family_update'),  
    path('families/<int:pk>/deactivate/', views.FamilyDeactivateView.as_view(), name='family_deactivate'),
    
]
 