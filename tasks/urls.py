from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import *

# url 
app_name='tasks'

urlpatterns = [
    path('tasks/<int:pk>', TaskDetail.as_view(), name='task_detail'),
    path('tasks/create', CreateTask.as_view(), name='create_task'),
    path('tasks/<int:pk>/update', UpdateTask.as_view(success_url=reverse_lazy('tasks:task_detail')),name='update_task'),  # TODO: need to specify task ID somewhere    
    path('tasks/delete', CreateTask.as_view(success_url=reverse_lazy('dashboard')), name='delete_task')
]
