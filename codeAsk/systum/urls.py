from django.urls import path
from .views import getQuestions, postQuestion, postAnswer, getAnswers, upvoteQuestion, downvoteQuestion, upvoteAnswer, downvoteAnswer

urlpatterns = [
    path('questions/', getQuestions, name='getQuestions'),
    path('questions/post/', postQuestion, name='postQuestion'),
    path('answers/post/', postAnswer, name='postAnswer'),
    path('answers/<int:question_id>/', getAnswers, name='getAnswers'),
    path('questions/<int:question_id>/upvote/', upvoteQuestion, name='upvoteQuestion'),
    path('questions/<int:question_id>/downvote/', downvoteQuestion, name='downvoteQuestion'),
    path('answers/<int:answer_id>/upvote/', upvoteAnswer, name='upvoteAnswer'),
    path('answers/<int:answer_id>/downvote/', downvoteAnswer, name='downvoteAnswer'),
]
