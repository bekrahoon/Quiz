from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Question(models.Model):
    text = models.CharField(max_length=255)  
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])

    def __str__(self):
        return self.text
    
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    score = models.IntegerField()
    total = models.IntegerField()
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total} on {self.date}"