from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Question, Result
from .forms import QuestionForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout


class CustomLoginView(View):
    def get(self, request):
        return render(request, 'login.html')  
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})

class CustomLogoutView(View):
    def post(self, request):  
        logout(request)
        return redirect('home')  
    
class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class QuestionListView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def get(self, request):
        questions = Question.objects.all()
        return render(request, 'question_list.html', {'questions': questions})

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


class QuizView(View):
    def get(self, request):
        questions = Question.objects.all()
        return render(request, 'quiz.html', {'questions': questions})

class QuizResultView(View):
    def post(self, request):
        questions = Question.objects.all()
        score = 0
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            if selected and int(selected) == question.correct_option:
                score += 1
        total = questions.count()
        
        if request.user.is_authenticated:
            Result.objects.create(
                user=request.user,
                score=score,
                total=total
            )
        
        return render(request, 'result.html', {'score': score, 'total': total})

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)  
        return render(request, 'profile_form.html', {'form': form})
    
    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')  
        return render(request, 'profile_form.html', {'form': form})
    
class ResultListView(LoginRequiredMixin, View):
    def get(self, request):
        results = Result.objects.filter(user=request.user).order_by('-date')
        return render(request, 'result_list.html', {'results': results})