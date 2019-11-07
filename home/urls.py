from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import *

# app_name='home'
urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),  
    # path('', )  
    path('signup/', SignUpView.as_view(success_url=reverse_lazy('home')), name='signup'),
    
    path('updateProfile/', UpdateUser.as_view(success_url=reverse_lazy('user_profile')),name='update_profile'),
    path('userProfile/',UserView.as_view(),name='user_profile'),
    
    path('dashboard/',TaskView.as_view(),name='dashboard'),
    path('transferOwnership/', TransferOwnership.as_view(success_url=reverse_lazy('team_view')),name='transfer_ownership'),
    
    path('newTeam/',CreateTeam.as_view(success_url=reverse_lazy('team_view')),name='new_team'),
    path('team/<int:pk>/deleteTeam/',RemoveTeam.as_view(success_url=reverse_lazy('dashboard')),name='delete_team'),
    path('team/<int:pk>/updateTeam/',UpdateTeam.as_view(success_url=reverse_lazy('team_view')),name='update_team'),
    path('team/<int:pk>/teamView/',TeamView.as_view(success_url=reverse_lazy('team_view')),name='team_view'),
   

    path('team/<int:pk>/addMember/',InviteMember.as_view(success_url=reverse_lazy('add_member')),name='add_member'),
    # path('promoteMember/',PromoteMember.as_view(success_url=reverse_lazy('promote_member')),name='promote_member'),
    # path('deleteMember/',DeleteMember.as_view(success_url=reverse_lazy('delete_member')),name='delete_member'),
]