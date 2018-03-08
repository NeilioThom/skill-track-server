from django.contrib.auth import authenticate, login, logout
from django.middleware import csrf
from django.db.models import FilteredRelation, Q
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from app.models import Skill, TimeEntry
from app.serializers import SkillSerializer, TimeEntrySerializer, LoginSerializer
import datetime

# Skills API
class Skills(APIView):
    # Can get one or multiple skills
    def get(self, request, skill_id=None, format=None):
        if(skill_id is not None):
            return(self.get_single_skill(request, skill_id=skill_id))

        return(self.get_multiple_skills(request))

    # Create a new skill
    def post(self, request, format=None):
        data = request.data

        serializer = SkillSerializer(data=data)

        if(serializer.is_valid()):
            serializer.save(user=request.user)

        return Response(serializer.data)

    # Updates an existing skill
    def put(self, request, skill_id=None, format=None):
        data = request.data
        skill = Skill.objects.get(pk=skill_id)

        # Make sure the skill belongs to this user
        if skill.user != request.user:
            return Response(status=404)
        
        skill_serialized = SkillSerializer(skill, data=data)

        if(skill_serialized.is_valid()):
            skill_serialized.save()

        return Response(skill_serialized.data)

    # Returns an array of multiple skills
    def get_multiple_skills(self, request):
        user = request.user
        skills = Skill.objects.filter(user=user).order_by('-id')
        

        # Serialize and return the final query
        skills_serialized = SkillSerializer(skills, many=True)
        return Response(skills_serialized.data)

    # Gets data about one single skill and entries
    def get_single_skill(self, request, skill_id=None):
        user = request.user

        try:
            skill = Skill.objects.get(pk=skill_id, user=user)
        except Skill.DoesNotExist:
            return Response(status=404)

        skill_serialized = SkillSerializer(skill)
        return Response(skill_serialized.data)

# Time Entries
class TimeEntries(APIView):
    def post(self, request, format=None):
        skill_id = request.GET.get('skill')
        data = request.data

        if skill_id is not None:
            skill = Skill.objects.get(pk=skill_id)

            if skill is not None:
                data['skill'] = skill

                serializer = TimeEntrySerializer(data)
                serializer.create(data)

                return Response(serializer.data)

    # GET entries for a skill
    def get(self, request, format=None):
        try:
            skill_id = request.GET.get('skill_id') or None
            page_num = int(request.GET.get('page')) or None
        except ValueError:
            return Response({ 'error': 'Invalid data type passed to API.' }, status=500)

        if skill_id is None or page_num is None:
            return Response({ 'error': 'Missing request parameters.' }, status=500)

        skill = Skill.objects.get(pk=skill_id)

        entries = TimeEntry.get_week_page(page=page_num, skill=skill)

        entries_serialized = TimeEntrySerializer(entries, many=True)

        return Response(entries_serialized.data)

# Authentication
class Auth(APIView):
    def post(self, request, format=None):
        auth_data = request.data

        username = auth_data['username'] or None
        password = auth_data['password'] or None

        if(username and password):
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                user_data = LoginSerializer(user).data
                return Response(user_data)

        return Response({ 'username': ['Invalid username or password.'] }, status=403)

    def delete(self, request, format=None):
        logout(request)
        return Response(status=200)


class IdentifyUser(APIView):
    def get(self, request, format=None):
        user = request.user

        if request.user.is_authenticated:
            return Response(LoginSerializer(user).data)

        return Response(status=403)
