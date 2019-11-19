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
from django.http import HttpResponseNotFound
from .helper import get_user_name_display

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
        managers_profile_id = Membership.objects.filter(role=1, team=team).values('user')
        manager_profile = UserProfile.objects.filter(id__in=managers_profile_id)

        employee_profile_id = Membership.objects.filter(role=100, team=team).values('user')
        employee_profile = UserProfile.objects.filter(id__in=employee_profile_id)
        ulist = UserProfile.objects.all()

        context = { 'team':team, 'summary': team.summary, 'managers' : manager_profile, 'employees': employee_profile, 'ulist': ulist}
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


<<<<<<< Updated upstream
class InviteMember(LoginRequiredMixin, View):  
    def post(self, request, pk):                
        userProfile_id_to_add = request.POST.get("user_id")
        print(pk)
        print(userProfile_id_to_add)
        team = Team.objects.get(id=pk)
        # user_to_add = User.objects.get(id=userProfile_id_to_add)
        userProfile = UserProfile.objects.get(user=userProfile_id_to_add)

        # TODO: verify correctness of the data
        member_exist = Membership.objects.filter(user=userProfile, team=team)
        if member_exist:
            pass
        if team.owner != request.user:
            print("user not owner!")        
            pass

        member = Membership(user=userProfile, team=team)
        member.save()
        print(member)        
        return redirect(reverse("team_detail", args=[pk]))
=======
class InviteMember(LoginRequiredMixin, View):
    
    pass
>>>>>>> Stashed changes
    

class PromoteMember(LoginRequiredMixin, UpdateView):
    pass


class DeleteMember(LoginRequiredMixin, DeleteView):
    pass


class TransferOwnership(LoginRequiredMixin, UpdateView):
    pass


############################################################
# Task-related Views

class TaskDetail(LoginRequiredMixin, View):
    model = Task
    template_name = "tasks/task_detail_page.html"

    def get(self, request, pk) :
        task = Task.objects.get(id=pk)
        user = request.user
        context = {
            "title": task.title, 
            "description": task.description,
            "results": task.results,
            "progress": task.get_progress_display(),
            "priority": task.get_priority_display(),
            "due_date": task.due_date
        }
        if (task.assigner == user):
            context["associate_user"] = get_user_name_display(task.worker)
            context["role"] = 1
        elif (task.worker == user):
            context["associate_user"] = get_user_name_display(task.assigner)
            context["role"] = 100
        else:
            return HttpResponseNotFound("Task not found!")
        
        return render(request, self.template_name, context)
     
    


class CreateTask(LoginRequiredMixin, CreateView):
    template_name = 'tasks/manager_team_form.html'
    model = Task
    fields = ['title', 'description', 'worker', 'priority', 'team', 'due_date']

    def form_valid(self, form):        
        print('form_valid called')
        task = form.save(commit=False)
        team.owner = self.request.user
        team.save()

        user_profile = UserProfile.objects.get(user=self.request.user)
        membership = Membership(user=user_profile, team=team, role=1)
        membership.save()
        return super(CreateTeam, self).form_valid(form)


class DeleteTask(LoginRequiredMixin, DeleteView):
    pass


class UpdateTask(LoginRequiredMixin, UpdateView):
    pass


