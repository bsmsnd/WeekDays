from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
class TaskDetail(LoginRequiredMixin, View):
    pass


class CreateTask(LoginRequiredMixin, CreateView):
    pass


class DeleteTask(LoginRequiredMixin, DeleteView):
    pass


class UpdateTask(LoginRequiredMixin, UpdateView):
    pass




