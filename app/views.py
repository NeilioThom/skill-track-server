from django.contrib.auth import authenticate, login
from django.middleware import csrf
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from app.models import Skill
from app.serializers import SkillSerializer, LoginSerializer

@api_view(['GET'])
def get_csrf(request):
    return Response(csrf.get_token(request))

# Skills API
@api_view(['GET', 'POST'])
def skills(request):
    if request.method == 'GET':
        skills = Skill.objects.all()
        skills_serialized = SkillSerializer(skills, many=True)
        return Response(skills_serialized.data)

    elif request.method == 'POST':
        serializer = SkillSerializer(data=request.data)

        if(serializer.is_valid()):
            serializer.save()

            skills = Skill.objects.all()
            skills_serialized = SkillSerializer(skills, many=True)
            return Response(skills_serialized.data)

        return Response(status=400)
return Response(status=403)

# Authentication
@api_view(['POST'])
def auth(request):
    if(request.method == 'POST'):
        print(request.user)
        auth_data = request.data

        username = auth_data['username'] or None
        password = auth_data['password'] or None

        if(username and password):
            user = authenticate(request, username=username, password=password)

            if user != None:
                login(request, user)
                user_data = LoginSerializer(user).data
                return Response("True")

    return Response(status=403)
