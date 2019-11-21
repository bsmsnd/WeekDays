from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .owner import *
from .helper import get_incomplete_task_choices, get_user_name_display
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.http.response import HttpResponseNotFound, HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils.dateparse import parse_date

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
        user_profile = UserProfile.objects.get(user=request.user)
        team = Team.objects.get(id=pk)
        #comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        #comment_form = CommentForm()
        managers_profile_id = Membership.objects.filter(role=1, team=team).values('user')
        manager_profile = UserProfile.objects.filter(id__in=managers_profile_id)

        employee_profile_id = Membership.objects.filter(role=100, team=team).values('user')
        employee_profile = UserProfile.objects.filter(id__in=employee_profile_id)
        ulist = UserProfile.objects.all()

        role = Membership.objects.get(team=team, user=user_profile).role
        context = { 'team':team, 'summary': team.summary, 'managers' : manager_profile, 'employees': employee_profile, 'ulist': ulist, 'role': role}
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
    def post(self, request, pk):                
        userProfile_id_to_add = request.POST.get("user_id")
        #print(pk)
        #print(userProfile_id_to_add)
        team = Team.objects.get(id=pk)
        # user_to_add = User.objects.get(id=userProfile_id_to_add)
        userProfile = UserProfile.objects.get(user=userProfile_id_to_add)
        
        # TODO: verify correctness of the data
        member_exist = Membership.objects.filter(user=userProfile, team=team)
        
        if team.owner != request.user:
            messages.error(request, 'Only team owner can add the team member!!')
            return redirect(reverse("team_detail", args=[pk]))
             
        if member_exist:
            messages.error(request, 'This user is alreay in the team')
            return redirect(reverse("team_detail", args=[pk]))

        member = Membership(user=userProfile, team=team)
        member.save()
        #print(member)        
        return redirect(reverse("team_detail", args=[pk]))
    

class PromoteMember(LoginRequiredMixin, UpdateView):
    pass


def promote_member(request, pk, pk2):
    userobj= UserProfile.objects.get(id = pk2)
    
    team_num = Team.objects.get(id=pk)
    memberrole = Membership.objects.get(user=userobj, team=team_num)
    print(memberrole)
    memberrole.role= 1
    memberrole.save()
    return redirect(reverse('team_detail', args=[pk]))



def remove_member(request, pk, pk2):
    userobj= get_object_or_404(UserProfile, id = pk2)
    team = Team.objects.get(id=pk)

    team.team_members.remove(userobj)
    team.save()
    return redirect(reverse('team_detail', args=[pk]))


def transfer_owner(request, pk, pk2):
    userobj= User.objects.get(id = pk2)
    team = Team.objects.get(id=pk)
    if team.owner != request.user:
        messages.error(request, 'You are not the owner')
        return redirect(reverse("team_detail", args=[pk]))
    else:
        team.owner = userobj
        print(team.owner)
    team.save()
    return redirect(reverse('team_detail', args=[pk]))


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
        context["task_id"] = pk
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
        # validation
        task = form.save(commit=False)
        task.assigner = self.request.user
        print('form_valid called')
        task.save()
        return super(CreateTask, self).form_valid(form)

class TestPreCreateTask(LoginRequiredMixin, View):
    template_name = 'tasks/precreate_choose_team.html'

    def get(self, request):
        userProfile = UserProfile.objects.get(user=request.user)
        managerTeams_id = Membership.objects.filter(user=userProfile, role=Membership.MANAGER).values('team')
        teams = Team.objects.filter(id__in=managerTeams_id)
        ctx = {'teams': teams}
        return render(request, self.template_name, ctx)


class TestCreateTask(LoginRequiredMixin, View):
    template_name = 'tasks/create_task.html'
    
    def get(self, request, pk):
        team = get_object_or_404(Team, id=pk)
        userProfile = UserProfile.objects.get(user=request.user)
        membership = get_object_or_404(Membership, user=userProfile, team=team)
        
        # not a member of the team, or the user is not a manager
        if not membership or membership.role == Membership.EMPLOYEE:
            return HttpResponseForbidden("You do not have access to the page")
        
        ulist = team.team_members.all()
        ctx = {'team': team, 'ulist': ulist}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        team = get_object_or_404(Team, id=pk)
        title = request.POST.get("title")
        desc = request.POST.get("request")
        employee_id = request.POST.get("employee")
        employee = get_object_or_404(UserProfile, id=employee_id).user
        priority = request.POST.get("priority")
        due_date = parse_date(request.POST.get("due_date"))
        
        task = Task(title=title, description=desc, assigner=request.user, worker=employee, priority=priority, team=team, due_date=due_date)
        task.save()
        return redirect('dashboard')


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/delete_task.html"


# This view is only for employee.
class UpdateTask(LoginRequiredMixin, UpdateView):
    template = "tasks/update_task.html"

    def get(self, request, pk):        
        task = get_object_or_404(Task, id=pk, worker=request.user)
        form = TaskEmployeeUpdateForm(instance=task)
        ctx = {
            'form': form, 
            'title': task.title, 
            'description': task.description, 
            'priority': task.get_priority_display(),
            'team': task.team, 
            'due_date': task.due_date, 
            'manager': get_user_name_display(task.assigner),
            'pk': pk
            }
        return render(request, self.template, ctx)
    
    def post(self, request, pk=None):    
        task = get_object_or_404(Task, id=pk, worker=self.request.user)
        form = TaskEmployeeUpdateForm(request.POST, request.FILES or None, instance=task)

        if not form.is_valid():
            ctx = {
                'form': form, 
                'title': task.title, 
                'description': task.description, 
                'priority': task.get_priority_display(),
                'team': task.team, 
                'due_date': task.due_date, 
                'manager': get_user_name_display(task.assigner),
                'pk': pk
                }
            return render(request, self.template, ctx)

        task.save()
        success_url = reverse_lazy('task_detail', args=[pk])
        
        return redirect(success_url)


# This view is only for manager
class EditTask(LoginRequiredMixin, UpdateView):
    template = "tasks/edit_task.html"

    def get(self, request, pk):        
        task = get_object_or_404(Task, id=pk, assigner=request.user)
        form = TaskManagerEditForm(instance=task)
        ctx = {
            'form': form, 
            'title': task.title, 
            'team': task.team, 
            'progress': task.get_progress_display(),
            'employee': get_user_name_display(task.worker),
            'pk': pk
            }
        return render(request, self.template, ctx)
    
    def post(self, request, pk=None):    
        task = get_object_or_404(Task, id=pk, assigner=self.request.user)
        form = TaskManagerEditForm(request.POST, request.FILES or None, instance=task)

        if not form.is_valid():
            ctx = {
                'form': form, 
                'title': task.title, 
                'team': task.team, 
                'progress': task.get_progress_display(),
                'employee': get_user_name_display(task.worker),
                'pk': pk
                }
            return render(request, self.template, ctx)

        task.save()
        success_url = reverse_lazy('task_detail', args=[pk])
        
        return redirect(success_url)


class DashboardView(LoginRequiredMixin, View):
    template = "tasks/dashboard.html"
    incomplete = get_incomplete_task_choices()

    def get(self, request):        
        # userProfile_id = UserProfile.objects.get(user=request.user)
        manager_task_list = Task.objects.filter(assigner=request.user)
        assigned_task_list = Task.objects.filter(worker=request.user)
        ctx = {
            "manager_task_list": manager_task_list,
            "assigned_task_list": assigned_task_list
        }
        return render(request, self.template, ctx)