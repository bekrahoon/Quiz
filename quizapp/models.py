from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)  # Текст вопроса
    option1 = models.CharField(max_length=100)  # Вариант 1
    option2 = models.CharField(max_length=100)  # Вариант 2
    option3 = models.CharField(max_length=100)  # Вариант 3
    option4 = models.CharField(max_length=100)  # Вариант 4
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])  # Правильный вариант (1-4)

    def __str__(self):
        return self.text