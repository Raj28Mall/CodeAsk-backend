from django.contrib import admin
from .models import Question, Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'upvotes', 'downvotes', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'body']
    ordering = ['-created_at']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'author_id', 'upvotes', 'downvotes', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['body']
    ordering = ['-created_at']
