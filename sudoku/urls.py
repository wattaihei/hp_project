from django.urls import path
from . import views

urlpatterns = [
        path('', views.question, name='next question'),
        path('answer', views.answer, name='answer'),
        ]