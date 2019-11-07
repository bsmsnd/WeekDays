from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

        def clean_username(self):
            username = self.cleaned_data['username']

            try:
                self.Meta.model.objects.get(username=username)
            except self.Meta.model.DoesNotExist:
                return username

            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):
    template_name='accounts/edit_profile.html'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )
