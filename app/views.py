from django.contrib.auth import authenticate, login
from django.middleware import csrf
from django.db.models import FilteredRelation, Q
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from app.models import Skill, TimeEntry
from app.serializers import SkillSerializer, LoginSerializer
import datetime
import pdb


# Skills API
class SkillsTest(APIView):
    def get(self, request, format=None):
        user = request.user

        skills = Skill.objects.filter(user=user).prefetch_related(
            Prefetch('entries', queryset=TimeEntry.objects.filter(created_date__date__gt=datetime.date.today() - datetime.timedelta(days=3)))
        ).all()

        skills_serialized = SkillSerializer(skills, many=True)
        return Response(skills_serialized.data)

    def post(self, request, format=None):
        data = request.data
        data['user'] = request.user

        serializer = SkillSerializer(data)

        serializer.create(data)

        return Response(serializer.data)

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

        return Response(status=403)

class IdentifyUser(APIView):
    def get(self, request, format=None):
        user = request.user

        if request.user.is_authenticated:
            return Response(LoginSerializer(user).data)

        return Response(status=403)
