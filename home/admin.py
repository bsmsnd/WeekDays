from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserProfile, Gender, Title, Team, Task, Membership, Tag, Message, Event,Invitee

# Register your models here.
# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['email', 'username',]

# admin.site.register(CustomUser, CustomUserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'gender', 'phone_number', 'title')

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-phone_number', 'user')
        return queryset    


class GenderAdmin(admin.ModelAdmin):
    list_display = ('name', )

    def get_queryset(self, request):
        queryset = super(GenderAdmin, self).get_queryset(request)        
        return queryset


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary')

    def get_queryset(self, request):
        queryset = super(TitleAdmin, self).get_queryset(request)        
        return queryset


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'owner')

    def get_queryset(self, request):
        queryset = super(TeamAdmin, self).get_queryset(request)        
        return queryset

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'results', 'progress', 'assigner_tag', 'worker_tag', 'assigner', 'worker', 'priority', 'team', 'due_date')
    # readonly_fields = ['due_date']
    def get_queryset(self, request):
        queryset = super(TaskAdmin, self).get_queryset(request)        
        return queryset

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role')
    def get_queryset(self, request):
        queryset = super(MembershipAdmin, self).get_queryset(request)        
        return queryset

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    def get_queryset(self, request):
        queryset = super(TagAdmin, self).get_queryset(request)        
        return queryset

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'starttime', 'endtime', 'location', 'host')
    def get_queryset(self, request):
        queryset = super(EventAdmin, self).get_queryset(request)        
        return queryset

class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'msg_time', 'status', 'sender', 'receiver')
    def get_queryset(self, request):
        queryset = super(MessageAdmin, self).get_queryset(request)        
        return queryset


class InviteeAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')
    def get_queryset(self, request):
        queryset = super(InviteeAdmin, self).get_queryset(request)        
        return queryset

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Invitee, InviteeAdmin)