from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class TaskView(LoginRequiredMixin, View):
    pass


class TeamView(LoginRequiredMixin, View):
    pass


class CreateTeam(LoginRequiredMixin, CreateView):
    pass


class UpdateTeam(LoginRequiredMixin, UpdateView):
    pass


class RemoveTeam(LoginRequiredMixin, DeleteView):
    pass


class InviteMember(LoginRequiredMixin, View):
    
    pass
    

class PromoteMember(LoginRequiredMixin, UpdateView):
    pass


class DeleteMember(LoginRequiredMixin, DeleteView):
    pass


class UserView(LoginRequiredMixin, View):
    model = CustomUser
    template_name = 'home/user_detail.html'


class UpdateUser(UserChangeForm):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('user_detail')
    template_name = 'signup.html'



class TransferOwnership(LoginRequiredMixin, UpdateView):
    pass



