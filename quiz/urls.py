from django.contrib import admin
from django.urls import path
from quizapp import views
from django.urls import reverse_lazy 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('questions/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
        # Quiz URLs
    path('quiz/', views.QuizView.as_view(), name='quiz'),
    path('quiz/result/', views.QuizResultView.as_view(), name='quiz_result'),
]