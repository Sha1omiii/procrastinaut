from django import forms
from .models import Project, Todo_Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
    
class Todo_TaskForm(forms.ModelForm):
    class Meta:
        model = Todo_Task
        fields = ['title', 'description', 'is_completed']