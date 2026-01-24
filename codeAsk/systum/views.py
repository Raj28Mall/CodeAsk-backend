from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Question, Answer
from .serializer import UserSerializer, QuestionSerializer, AnswerSerializer

@api_view(['GET'])
def getQuestions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def postQuestion(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def postAnswer(request):
    serializer = AnswerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getAnswers(request, question_id):
    answers = Answer.objects.filter(question_id=question_id)
    serializer = AnswerSerializer(answers, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def upvoteQuestion(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.upvotes += 1
        question.save()
        return Response({'message': 'Question upvoted successfully'}, status=status.HTTP_200_OK)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def downvoteQuestion(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.downvotes += 1
        question.save()
        return Response({'message': 'Question downvoted successfully'}, status=status.HTTP_200_OK)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def upvoteAnswer(request, answer_id):
    try:
        answer = Answer.objects.get(id=answer_id)
        answer.upvotes += 1
        answer.save()
        return Response({'message': 'Answer upvoted successfully'}, status=status.HTTP_200_OK)
    except Answer.DoesNotExist:
        return Response({'error': 'Answer not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def downvoteAnswer(request, answer_id):
    try:
        answer = Answer.objects.get(id=answer_id)
        answer.downvotes += 1
        answer.save()
        return Response({'message': 'Answer downvoted successfully'}, status=status.HTTP_200_OK)
    except Answer.DoesNotExist:
        return Response({'error': 'Answer not found'}, status=status.HTTP_404_NOT_FOUND)


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