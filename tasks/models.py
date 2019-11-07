from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from home.models import CustomUser, Team
from django.contrib.auth.models import User


# Create your models here.
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
    progress = models.PositiveSmallIntegerField(
        default=0, 
        validators=[MaxValueValidator(100)],
    )
    assigner_tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    worker_tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    assigner = models.ForeignKey(User, on_delete=models.CASCADE)
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    due_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )

    def __str__(self):
        return self.name