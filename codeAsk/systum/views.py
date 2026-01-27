from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Question, Answer

@csrf_exempt
def signupUser(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        pwd = data.get('password')
        user = User.objects.create_user(username = username, password = pwd)
        user.save()
        return JsonResponse({'message' : 'User created successfully'}, status = 200)

@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        pwd = data.get('password')
        user = authenticate(request, username = username, password = pwd)

        if user is not None:
            login(request, user)
            return JsonResponse({'message' : 'Logged in successfully', 'username': user.username}, status = 200)
        else:
            return JsonResponse({'error' : 'Invalid username password combination'}, status = 401)