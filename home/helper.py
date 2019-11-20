# This file saves all helper functions of the project

from django.contrib.auth.models import User
from .models import Task

def get_user_name_display(user):
    # this function return a formatted display of user's name and username
    # :param: user: an instance of user
    # :return: formatted display, last_name first_name (username)
    # e.g. Jack Chen (jack123)

    return user.last_name + " " + user.first_name + " " + "(%s)" % user.username

def get_incomplete_task_choices():
    progress_to_choice = Task.PROGRESS_CHOICES
    return list(dict(progress_to_choice).keys())[:-1]