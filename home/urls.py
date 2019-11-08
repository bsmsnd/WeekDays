from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from django.conf.urls import url
from .views import *
# from django.contrib.auth.views import (
#     login, logout, password_reset, password_reset_done, password_reset_confirm,
#     password_reset_complete
# )
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

# app_name='home'
urlpatterns = [
    # path('', LoginView.as_view(template_name='accounts/login.html'),name='home'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),    
    path('accounts/login/', LoginView.as_view(template_name='accounts/login.html'),name='accounts_login'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'),name='logout'),            
    path('register/', SignUpView.as_view(success_url=reverse_lazy('login')),name='register'),            
    # url(r'^register/$', register, name='register'),
    url(r'^profile/$', view_profile, name='view_profile'),
    url(r'^profile/(?P<pk>\d+)/$', view_profile, name='view_profile_with_pk'),
    url(r'^profile/edit/$', edit_login_profile, name='edit_login_profile'),
    url(r'profile/update/$',UserProfileUpdateView.as_view(), name='edit_user_profile'),
    url(r'^change-password/$', change_password, name='change_password'),
    
    re_path(r'^reset-password/$', PasswordResetView.as_view(template_name='accounts/reset_password.html'),name='reset_password'),
    
    re_path(r'^reset-password/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('reset-password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('reset-password/completes/', PasswordResetDoneView.as_view(), name='password_reset_complete'),

    # path('', )  
    # path('signup/', SignUpView.as_view(success_url=reverse_lazy('home')), name='signup'),
    
    # path('updateProfile/', UpdateUser.as_view(success_url=reverse_lazy('user_profile')),name='update_profile'),
    # path('userProfile/',UserView.as_view(),name='user_profile'),
    ## --------------------------------------------------------

    # path('dashboard/',TaskView.as_view(),name='dashboard'),
    # path('transferOwnership/', TransferOwnership.as_view(success_url=reverse_lazy('team_view')),name='transfer_ownership'),
    
    # path('newTeam/',CreateTeam.as_view(success_url=reverse_lazy('team_view')),name='new_team'),
    # path('team/<int:pk>/deleteTeam/',RemoveTeam.as_view(success_url=reverse_lazy('dashboard')),name='delete_team'),
    # path('team/<int:pk>/updateTeam/',UpdateTeam.as_view(success_url=reverse_lazy('team_view')),name='update_team'),
    # path('team/<int:pk>/teamView/',TeamView.as_view(success_url=reverse_lazy('team_view')),name='team_view'),
   

    # path('team/<int:pk>/addMember/',InviteMember.as_view(success_url=reverse_lazy('add_member')),name='add_member'),

    ## --------------------------------------------------------
    # path('promoteMember/',PromoteMember.as_view(success_url=reverse_lazy('promote_member')),name='promote_member'),
    # path('deleteMember/',DeleteMember.as_view(success_url=reverse_lazy('delete_member')),name='delete_member'),
]