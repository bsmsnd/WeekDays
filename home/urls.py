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
    # path('accounts/login/', LoginView.as_view(template_name='index.html'), name='accounts_login'),    
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
    
]
 
 # Tasks
urlpatterns += [
    path('tasks/<int:pk>', TaskDetail.as_view(), name='task_detail'),
    path('tasks/create', CreateTask.as_view(success_url=reverse_lazy('dashboard')), name='create_task'),
    path('tasks/<int:pk>/edit', EditTask.as_view(),name='edit_task'),
    path('tasks/<int:pk>/update', UpdateTask.as_view(),name='update_task'),  # TODO: need to specify task ID somewhere    
    path('tasks/<int:pk>/delete', DeleteTask.as_view(success_url=reverse_lazy('dashboard')),name='delete_task'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('test', TestPreCreateTask.as_view(), name='pre_create_task'),
    path('test/<int:pk>', TestCreateTask.as_view(), name='create_task_with_team_id'),
]

# Teams
urlpatterns += [
    path('myTeams/', TeamListView.as_view(), name='team_list'),
    path('teams/<int:pk>', TeamDetailView.as_view(), name='team_detail'),
    path('teams/<int:pk>/update', UpdateTeam.as_view(), name='team_update'),
    path('teams/<int:pk>/addMember',InviteMember.as_view(), name="add_user"),
    url(r'^teams/(?P<pk>[0-9]+)/promoteMember/(?P<pk2>[0-9]+)$', promote_member, name='promote_member'),
    url(r'^teams/(?P<pk>[0-9]+)/deleteMember/(?P<pk2>[0-9]+)$', remove_member, name='delete_member'),
    url(r'^teams/(?P<pk>[0-9]+)/transferOwner/(?P<pk2>[0-9]+)$', transfer_owner, name='transfer_owner'),
    path('teams/create', CreateTeam.as_view(success_url=reverse_lazy('team_list')), name='team_create'),
    path('teams/<int:pk>/remove', RemoveTeam.as_view(success_url=reverse_lazy('team_list')), name='team_remove'),

    
]


# Events
urlpatterns += [
    path('events/create', CreateEventView.as_view(), name="create_event"),
    path('events/<int:pk>', EventDetailView.as_view(), name="event_detail"), 
    path('events/<int:pk>/update', EventUpdateView.as_view(), name="event_update"),
    path('events/<int:pk>/delete', EventDeleteView.as_view(success_url=reverse_lazy('dashboard')), name="event_delete"), 
]

# Messages
urlpatterns += [
    path('message/create', MessageCreateView.as_view(), name="create_message"),
    path('message/<int:pk>/delete', MessageDeleteView.as_view(success_url=reverse_lazy('message_list')), name="delete_message"),
    path('message/<int:pk>', MessageDetailView.as_view(), name="message_detail"), 
    path('message', MessageListView.as_view(), name="message_list"),
]
