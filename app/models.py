from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
import datetime

# Create your models here.
class Skill(models.Model):
    class Meta():
        db_table = 'Skill'

    name = models.CharField(max_length=100)
    weekly_goal = models.IntegerField()
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    def create(self, validated_data):
        skill = Skill(
            name=validated_data['name'],
            user=validated_data['user'],
            entries=[]
        )

    def withDate(self):
        return self.entries.filter(entries__created_date__gt=datetime.datetime.now() - datetime.timedelta(days=7))

        skill.save()
        return skill

    def __str__(self):
        return self.name

class TimeEntry(models.Model):
    class Meta():
        db_table = 'TimeEntry'
        verbose_name_plural = "Time Entries"

    time_spent = models.IntegerField()
    comment = models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now=True)
    skill = models.ForeignKey(Skill, related_name='entries', on_delete=models.CASCADE)

    def __str__(self):
        return "Entry " + str(self.id) + " for " + self.skill.name
