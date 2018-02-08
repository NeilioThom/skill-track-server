from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.
class Skill(models.Model):
    class Meta():
        db_table = 'Skill'

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TimeEntry(models.Model):
    class Meta():
        db_table = 'TimeEntry'

    duration = models.IntegerField()
    created_date = models.DateField()
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
