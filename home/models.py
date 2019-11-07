from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save

# Create your models here.
# class UserProfileManager(models.Manager):
#     def get_queryset(self):
#         return super(UserProfileManager, self).get_queryset()


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.ForeignKey('Gender', on_delete=models.SET_NULL, null=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    title = models.ForeignKey('Title', on_delete=models.SET_NULL, null=True)    
    # london = UserProfileManager()

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


# class CustomUser(AbstractUser):
#     """ Model representation of an User """

#     # first_name = models.CharField(max_length=100)
#     # middle_name = models.CharField(max_length=100, null=True, blank=True)
#     # last_name = models.CharField(max_length=100)
#     date_of_birth = models.DateField(null=True, blank=True)
#     #age = models.PositiveSmallIntegerField(default=20)
#     gender = models.ForeignKey('Gender', on_delete=models.SET_NULL, null=True)
#     phone_number = PhoneNumberField(null=True, blank=True)
#     title = models.ForeignKey('Title', on_delete=models.SET_NULL, null=True)    

#     # add additional fields in here

#     def __str__(self):
#         return self.email


class Gender(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, help_text='Enter a brief summary of the title', null=True, blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, help_text='Enter a brief summary of the team', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.BooleanField()  # manager = 1; employee = 0