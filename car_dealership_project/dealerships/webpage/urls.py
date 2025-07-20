# webpage/urls.py

from django.urls import path
from . import views

app_name = 'webpage'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'), # [cite: 166]
    path('contact/', views.contact, name='contact'), # [cite: 165]
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]