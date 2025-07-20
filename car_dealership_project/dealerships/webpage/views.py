# webpage/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def index(request):
    return render(request, 'webpage/index.html')

def about(request):
    return render(request, 'webpage/about.html') # 

def contact(request):
    return render(request, 'webpage/contact.html') # 

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!") # 
                return redirect('webpage:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'webpage/login.html', {'form': form})

def logout_view(request):
    messages.info(request, "You have been logged out.") # 
    logout(request)
    return redirect('webpage:index')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!") # 
            return redirect('webpage:index')
        else:
            messages.error(request, "Error creating account. Please check your input.")
    else:
        form = UserCreationForm()
    return render(request, 'webpage/signup.html', {'form': form})