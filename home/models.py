from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

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
    teams = models.ManyToManyField('Team', through='Membership')
    # london = UserProfileManager()

    def __str__(self):
        return self.user.username

    def display_name(self):
        return self.user.first_name + " " + self.user.last_name + " (%s)" % self.user.username

    def diaplay_name_and_email(self):
        return self.user.first_name + " " + self.user.last_name + " (%s)" % self.user.email


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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    team_members = models.ManyToManyField(UserProfile, through='Membership', related_name='team_members')
    
    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    MANAGER = 1
    EMPLOYEE = 100

    MEMBER_CHOICE = (
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee'),
    )

    role = models.IntegerField(choices=MEMBER_CHOICE, default=EMPLOYEE)
   

    def __str__(self):
        return "User " + str(self.user.id) + " <--> Team" + str(self.team.id)


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    description = models.CharField(
        max_length=1000,        
        null=True, blank=True     
    )
    results = models.CharField(
        max_length=1000,        
        null=True, blank=True     
    )

    PROGRESS_CHOICES = (
        (1, 'Not started'),
        (2, '~25%'),
        (3, '~50%'),
        (4, '~75%'),
        (5, 'Completed')
    )

    progress = models.PositiveSmallIntegerField(
        choices=PROGRESS_CHOICES, default=1,        
    )

    assigner_tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, related_name='assigner_tag')
    worker_tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, related_name='worker_tag')
    assigner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigner')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee')
    
    PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    )
    
    priority = models.PositiveSmallIntegerField(
        choices=PRIORITY_CHOICES, default=1,        
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    due_date = models.DateField()

    def __str__(self):
        return self.title


