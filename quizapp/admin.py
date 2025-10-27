from django.contrib import admin
from .models import Question

admin.site.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'correct_option')
    search_fields = ('text',)