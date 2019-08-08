from django.urls import path
from . import views

urlpatterns = [
    path('', views.Question, name='question'),
    path('answer', views.Answer, name='answer'),
]