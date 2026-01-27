from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from .models import Question, Answer, Vote
from .serializer import (
    UserSerializer,
    QuestionListSerializer,
    QuestionDetailSerializer,
    QuestionCreateSerializer,
    AnswerSerializer,
    AnswerCreateSerializer,
    VoteSerializer,
)




@api_view(['GET'])
@permission_classes([AllowAny])
def question_list_view(request):
    questions = Question.objects.all()
    serializer = QuestionListSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ask_question_view(request):
    serializer = QuestionCreateSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save(author=request.user)
        return Response(
            QuestionListSerializer(question).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def question_detail_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    serializer = QuestionDetailSerializer(question)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def answer_create_view(request):
    serializer = AnswerCreateSerializer(data=request.data)
    if serializer.is_valid():
        question = get_object_or_404(
            Question,
            pk=serializer.validated_data['question_id']
        )
        answer = Answer.objects.create(
            question=question,
            body=serializer.validated_data['body'],
            author=request.user
        )
        return Response(
            AnswerSerializer(answer).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_view(request):
    """
    Logic:
        - If vote exists and type matches: Remove vote.
        - If vote exists and type differs: Update vote type.
        - If vote doesn't exist: Create new vote.
    """
    from .models import Vote
    from .serializer import VoteSerializer

    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        model_type = data['model_type']
        model_id = data['model_id']
        vote_type = data['vote_type']
        user = request.user
        
        if model_type == 'question':
            target = get_object_or_404(Question, pk=model_id)
            lookup = {'question': target, 'answer': None}
        else:
            target = get_object_or_404(Answer, pk=model_id)
            lookup = {'question': None, 'answer': target}
            
        vote = Vote.objects.filter(user=user, **lookup).first()
        
        if vote:
            if vote.vote_type == vote_type:
                vote.delete()
                if vote_type == 'UP':
                    target.upvotes = max(0, target.upvotes - 1)
                else:
                    target.downvotes = max(0, target.downvotes - 1)
                target.save()
                return Response({'status': 'vote removed'})
            else:
                old_type = vote.vote_type
                vote.vote_type = vote_type
                vote.save()
                if vote_type == 'UP': 
                    target.upvotes += 1
                    target.downvotes = max(0, target.downvotes - 1)
                else: 
                    target.downvotes += 1
                    target.upvotes = max(0, target.upvotes - 1)
                target.save()
                return Response({'status': 'vote updated'})
        else:
            Vote.objects.create(
                user=user,
                vote_type=vote_type,
                **lookup
            )
            if vote_type == 'UP':
                target.upvotes += 1
            else:
                target.downvotes += 1
            target.save()
            return Response({'status': 'vote created'}, status=status.HTTP_201_CREATED)
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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