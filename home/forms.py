from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField

from .models import UserProfile
from django.utils.translation import gettext, gettext_lazy as _


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
    password = None
    template_name='accounts/edit_login_profile.html'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            # 'password'
            # 'title'
        )


class CreateForm(forms.ModelForm):
    # max_upload_limit = 2 * 1024 * 1024
    # max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    # picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    # upload_field_name = 'picture'

    class Meta:
        model = UserProfile
        fields = ['title','gender','date_of_birth','phone_number'] 

    # Validate the size of the picture
    def clean(self) :
        cleaned_data = super().clean()
        # pic = cleaned_data.get('picture')
        # if pic is None : return
        # if len(pic) > self.max_upload_limit:
        #     self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")
            
    # Convert uploaded File object to a picture
    def save(self, commit=True) :
        instance = super(CreateForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        # f = instance.picture   # Make a copy
        # if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
        #     bytearr = f.read();
        #     instance.content_type = f.content_type
        #     instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


