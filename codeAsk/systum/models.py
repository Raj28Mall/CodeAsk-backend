from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answers')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Answer to: {self.question.title[:50]}"
    
class Vote(models.Model):
    VOTE_TYPE_CHOICES = (
        ('UP', 'Upvote'),
        ('DOWN', 'Downvote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE, related_name='votes')
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('user', 'question'),
            ('user', 'answer'),
        ]

    def __str__(self):
        target = f"Question {self.question.id}" if self.question else f"Answer {self.answer.id}"
        return f"{self.user.username} {self.vote_type} on {target}"
    

