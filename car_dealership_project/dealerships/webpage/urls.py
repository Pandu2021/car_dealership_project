# webpage/urls.py

from django.urls import path
from . import views

app_name = 'webpage'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'), 
    path('contact/', views.contact, name='contact'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('dealers/', views.dealer_list, name='dealer_list'),
    path('dealer/<int:dealer_id>/', views.dealer_detail, name='dealer_detail'),
    path('dealer/<int:dealer_id>/review/', views.add_review_form, name='add_review_form'),
    path('cars/', views.carmake_list, name='cars'),
    path('sentiment/', views.sentiment_view, name='sentiment'),
    path('dealersbystate/<str:state>/', views.dealer_by_state, name='dealers_by_state'),  

]
