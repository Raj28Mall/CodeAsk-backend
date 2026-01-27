from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Question, Answer, Vote

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username']



class AnswerSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Answer
        fields = ['id', 'body', 'author', 'upvotes', 'downvotes', 'created_at']
        read_only_fields = ['id', 'author', 'upvotes', 'downvotes', 'created_at']


class QuestionListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    answer_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'author', 'upvotes', 'downvotes', 'created_at', 'answer_count']
        read_only_fields = ['id', 'author', 'upvotes', 'downvotes', 'created_at']
    
    def get_answer_count(self, obj):
        return obj.answers.count()


class QuestionDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'author', 'upvotes', 'downvotes', 'created_at', 'answers']
        read_only_fields = ['id', 'author', 'upvotes', 'downvotes', 'created_at', 'answers']


class QuestionCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ['title', 'body']


class AnswerCreateSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Answer
        fields = ['question_id', 'body']


class VoteSerializer(serializers.Serializer):
    model_type = serializers.ChoiceField(choices=['question', 'answer'])
    model_id = serializers.IntegerField()
    vote_type = serializers.ChoiceField(choices=['UP', 'DOWN'])


