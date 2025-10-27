from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Question
from .forms import QuestionForm  # Создадим форму ниже


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

# Read: Список вопросов
class QuestionListView(View):
    def get(self, request):
        questions = Question.objects.all()
        return render(request, 'question_list.html', {'questions': questions})

# Create: Добавление вопроса
class QuestionCreateView(View):
    def get(self, request):
        form = QuestionForm()
        return render(request, 'question_form.html', {'form': form})
    
    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
        return render(request, 'question_form.html', {'form': form})

# Update: Редактирование вопроса
class QuestionUpdateView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = QuestionForm(instance=question)
        return render(request, 'question_form.html', {'form': form})
    
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_list')
        return render(request, 'question_form.html', {'form': form})

# Delete: Удаление вопроса
class QuestionDeleteView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        return render(request, 'question_confirm_delete.html', {'question': question})
    
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        return redirect('question_list')
    
# Quiz: Главная страница игры
class QuizView(View):
    def get(self, request):
        questions = Question.objects.all()
        return render(request, 'quiz.html', {'questions': questions})

# Результат: Обработка ответов (POST)
class QuizResultView(View):
    def post(self, request):
        questions = Question.objects.all()
        score = 0
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            if selected and int(selected) == question.correct_option:
                score += 1
        total = questions.count()
        return render(request, 'result.html', {'score': score, 'total': total})