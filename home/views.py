from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'

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

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

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


# class UserView(LoginRequiredMixin, View):
#     model = CustomUser
#     template_name = 'home/user_detail.html'


# class UpdateUser(UserChangeForm):
#     form_class = CustomUserChangeForm
#     success_url = reverse_lazy('user_detail')
#     template_name = 'signup.html'

class TransferOwnership(LoginRequiredMixin, UpdateView):
    pass



