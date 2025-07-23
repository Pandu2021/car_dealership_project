# webpage/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
import requests
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .models import CarMake
from textblob import TextBlob

def dealer_by_state(request, state):
    response = requests.get(f"http://localhost:3000/fetchDealersByState/{state}")
    dealers = response.json()
    return render(request, 'webpage/dealer_list.html', {'dealers': dealers})

def sentiment_view(request):
    text = request.GET.get('text', '')
    polarity = TextBlob(text).sentiment.polarity
    sentiment = 'positive' if polarity > 0 else 'negative' if polarity < 0 else 'neutral'
    return JsonResponse({ 'sentiment': sentiment, 'polarity': polarity })

def carmake_list(request):
    carmakes = CarMake.objects.all()
    return render(request, 'webpage/cars.html', { 'carmakes': carmakes })

def dealer_list(request):
    response = requests.get("http://localhost:3000/fetchDealers")
    dealers = response.json()
    return render(request, 'webpage/dealer_list.html', {'dealers': dealers})

def dealer_detail(request, dealer_id):
    dealer = requests.get(f"http://localhost:3000/fetchDealer/{dealer_id}").json()
    reviews = requests.get(f"http://localhost:3000/fetchReview/dealer/{dealer_id}").json()
    return render(request, 'webpage/dealer_detail.html', {'dealer': dealer, 'reviews': reviews})

def add_review_form(request, dealer_id):
    dealer = requests.get(f"http://localhost:3000/fetchDealer/{dealer_id}").json()
    if request.method == "POST":
        payload = {
            "dealership": dealer_id,
            "name": request.POST.get("name"),
            "review": request.POST.get("review"),
            "purchase": bool(request.POST.get("purchase")),
            "car_make": "Toyota",
            "car_model": "Yaris",
            "car_year": 2021
        }
        requests.post("http://localhost:3000/insertReview", json=payload)
        return HttpResponseRedirect(f"/dealer/{dealer_id}/")
    return render(request, 'webpage/add_review_form.html', {'dealer': dealer})

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