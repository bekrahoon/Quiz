from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Question
from .forms import QuestionForm 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout

# Кастомный login (без встроенного LoginView)
class CustomLoginView(View):
    def get(self, request):
        return render(request, 'login.html')  # Показ формы
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect на home после login
        else:
            # Ошибка: неверные credentials
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})

# Кастомный logout (без встроенного LogoutView)
class CustomLogoutView(View):
    def post(self, request):  # Только POST для безопасности
        logout(request)
        return redirect('home')  # Redirect на home после logout
    
# Регистрация пользователя
class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirect на login после регистрации

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# Read: Список вопросов (только для админов)
class QuestionListView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def get(self, request):
        questions = Question.objects.all()
        return render(request, 'question_list.html', {'questions': questions})

# Create: Добавление вопроса (только для админов)
class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def get(self, request):
        form = QuestionForm()
        return render(request, 'question_form.html', {'form': form})
    
    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
        return render(request, 'question_form.html', {'form': form})

# Update: Редактирование вопроса (только для админов)
class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
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

# Delete: Удаление вопроса (только для админов)
class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        return render(request, 'question_confirm_delete.html', {'question': question})
    
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        return redirect('question_list')

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


    
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