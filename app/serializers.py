from django.contrib.auth.models import User
from rest_framework import serializers
from app.models import Skill, TimeEntry

class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        exclude = ('skill',)

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = ('user',)

    entries = TimeEntrySerializer(many=True, read_only=True)

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
