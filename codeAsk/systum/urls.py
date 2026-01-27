from django.urls import path
from .views import (
    question_list_view,
    question_detail_view,
    ask_question_view,
    answer_create_view,
    vote_view,
)

urlpatterns = [
    path('questions/', question_list_view, name='question-list'),
    path('questions/<int:pk>/', question_detail_view, name='question-detail'),
    path('ask/', ask_question_view, name='ask-question'),
    path('answer/', answer_create_view, name='answer-create'),
    path('vote/', vote_view, name='vote'),
]
