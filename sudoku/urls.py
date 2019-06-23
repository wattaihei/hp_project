from django.urls import path
from . import views

urlpatterns = [
        path('', views.home, name='home'),
        path('question/<int:num>', views.question, name='question'),
        path('answer/<int:num>', views.answer, name='answer'),
        ]