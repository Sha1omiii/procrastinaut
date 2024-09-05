from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Project, Todo_Task
from .forms import ProjectForm, Todo_TaskForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm();
    
    return render(request, 'registration/signup.html', {'form': form})

def home(request):
    return render(request, 'projects_page/home.html')

@login_required
def profile(request):
    user = request.user
    return render(request, 'registration/profile.html', {'user': user})

#handles showing all the projects created by the logged in user
@login_required
def list_project(request): 
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'projects_page/list_project.html', {'projects': projects})

#handles creating a new project 
@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid(): 
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('list_project')
    else:
        form = ProjectForm()
    return render(request, 'projects_page/project_form.html', {'form': form})    

#show a specific projects page 
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    return render(request, 'projects_page/project_detail.html', {'project': project})

# updating an exisiting project file
@login_required
def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects_page/project_form.html', {'form': form})

# delete
@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('list_project')
    return render(request, 'projects_page/confirm_delete.html', {'project': project})


# now for tasks 
@login_required
def create_todo_task(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, owner=request.user)
    if request.method == 'POST':
        form = Todo_TaskForm(request.POST)
        if form.is_valid():
            todo_task = form.save(commit=False)
            todo_task.project = project
            todo_task.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = Todo_TaskForm()
    return render(request, 'projects_page/todo_task_form.html', {'form': form, 'project': project})

@login_required
def update_todo_task(request, project_pk, todo_task_pk):
    project = get_object_or_404(Project, pk=project_pk, owner=request.user)
    todo_task = get_object_or_404(Todo_Task, pk=todo_task_pk, project=project)
    if request.method == 'POST':
        form = Todo_TaskForm(request.POST, instance=todo_task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project_pk)
    else:
        form = Todo_TaskForm(instance=todo_task)
    return render(request, 'projects_page/todo_task_form.html', {'form': form, 'project': project})

@login_required
def delete_todo_task(request, project_pk, todo_task_pk):
    project = get_object_or_404(Project, pk=project_pk, owner=request.user)
    todo_task = get_object_or_404(Todo_Task, pk=todo_task_pk, project=project)
    if request.method == 'POST':
        todo_task.delete()
        return redirect('project_detail', pk=project.pk)
    return render(request, 'projects_page/todo_task_delete.html', {'todo_task': todo_task, 'project': project})