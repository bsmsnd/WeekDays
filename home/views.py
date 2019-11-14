from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .owner import *
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/reg_form.html'

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)

@login_required
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
        user_profile = UserProfile.objects.get(user=user)
    else:
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
    args = {'user': user, 'user_profile': user_profile}
    return render(request, 'accounts/profile.html', args)

@login_required
def edit_login_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_login_profile.html', args)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('view_profile'))
        else:
            return redirect(reverse('change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)



class UserProfileUpdateView(LoginRequiredMixin, View):
    template = "accounts/edit_user_profile.html"
    success_url = reverse_lazy('view_profile')
    
    def get(self, request):
        userprofile = UserProfile.objects.get(user=request.user)        
        form = CreateForm(instance=userprofile)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        userprofile = UserProfile.objects.get(user=request.user)
        form = CreateForm(request.POST, instance=userprofile)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)                
        
        # Add owner to the model before saving
        userprofile = form.save(commit=False)        
        userprofile.save()
        
        return redirect(self.success_url)


class TaskView(LoginRequiredMixin, generic.ListView):
    pass


class TeamListView(LoginRequiredMixin, generic.ListView):
    template = "teams/my_teams.html"
    model = Team

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        teams = user_profile.teams.all()
        context = {'teams' : teams}
        return render(request, self.template, context)


class TeamDetailView(LoginRequiredMixin, View):
    model = Team
    template_name = "teams/team_detail.html"

    def get(self, request, pk) :
        team = Team.objects.get(id=pk)
        #comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        #comment_form = CommentForm()
        
        context = { 'team':team, 'summary': team.summary}
        return render(request, self.template_name, context)


class CreateTeam(generic.CreateView):
    template_name = 'teams/team_form.html'
    model = Team
    fields = ['name', 'summary']

    def form_valid(self, form):        
        print('form_valid called')
        team = form.save(commit=False)
        team.owner = self.request.user
        team.save()

        user_profile = UserProfile.objects.get(user=self.request.user)
        membership = Membership(user=user_profile, team=team, role=1)
        membership.save()
        return super(CreateTeam, self).form_valid(form)


class UpdateTeam(OwnerUpdateView):
    template_name = 'teams/team_form.html'
    model = Team
    fields = ['name', 'summary']


class RemoveTeam(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = "teams/delete_team.html"


class InviteMember(LoginRequiredMixin, View):    
    pass
    

class PromoteMember(LoginRequiredMixin, UpdateView):
    pass


class DeleteMember(LoginRequiredMixin, DeleteView):
    pass


class TransferOwnership(LoginRequiredMixin, UpdateView):
    pass


############################################################
# Task-related Views

class TaskDetail(LoginRequiredMixin, View):
    pass


class CreateTask(LoginRequiredMixin, CreateView):
    pass


class DeleteTask(LoginRequiredMixin, DeleteView):
    pass


class UpdateTask(LoginRequiredMixin, UpdateView):
    pass


