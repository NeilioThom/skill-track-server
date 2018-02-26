from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
from datetime import date, timedelta

class Skill(models.Model):
    class Meta():
        db_table = 'Skill'

    name = models.CharField(max_length=100)
    weekly_goal = models.IntegerField()
    total_time_spent = models.IntegerField()
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now=True)

    def create(self, validated_data):
        skill = Skill(
            name=validated_data['name'],
            user=validated_data['user'],
            entries=[]
        )

    # Updates the total amount of time spent every time the model is saved
    def update_time_spent(self):
        self.total_time_spent = sum(item.time_spent for item in self.entries.all())

    def save(self, *args, **kwargs):
        self.update_time_spent()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class TimeEntry(models.Model):
    class Meta():
        db_table = 'TimeEntry'
        ordering = ('-created_date',)
        verbose_name_plural = "Time Entries"

    time_spent = models.IntegerField()
    comment = models.CharField(max_length=1000)
    created_date = models.DateField()
    skill = models.ForeignKey(Skill, related_name='entries', on_delete=models.CASCADE)


    ## Method to get entries from X number of weeks ago, where weeks is the page argument
    @classmethod
    def get_week_page(self, *args, **kwargs):
        skill = kwargs.get('skill')
        date_page = kwargs.get('page') - 1

        this_week_start = date.today() - timedelta(days=date.today().weekday())
        date_start = this_week_start - timedelta(days=date_page * 7)
        date_end = date_start + timedelta(days=7)

        return self.objects.filter(skill=skill).filter(Q(created_date__gt=date_start), Q(created_date__lt=date_end))

    def save(self, *args, **kwargs):
        saved_item = super().save(*args, **kwargs)
        saved_skill = self.skill.save()
        return saved_item

    def __str__(self):
        return "Entry " + str(self.id) + " for " + self.skill.name
