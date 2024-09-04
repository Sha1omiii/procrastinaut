from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

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
    return render(request, 'page/home.html')

@login_required
def profile(request):
    user = request.user
    return render(request, 'registration/profile.html', {'user': user})