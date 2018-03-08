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

    id = serializers.UUIDField(read_only=True)
    total_time_spent = serializers.IntegerField(read_only=True)
    entries = TimeEntrySerializer(many=True, default=[], read_only=True)

    def create(self, validated_data):
        print(validated_data)
        return Skill.objects.create(
            name=validated_data['name'],
            weekly_goal=validated_data['weekly_goal'],
            user=validated_data['user']
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.weekly_goal = validated_data.get('weekly_goal', instance.weekly_goal)  
        instance.save()

        return instance

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
