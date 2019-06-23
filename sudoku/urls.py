from django.urls import path
from . import views

urlpatterns = [
        path('', views.home, name='home'),
        path('delete', views.delete, name='delete'),
        path('question/<int:num>', views.question, name='question'),
        path('answer/<int:num>', views.answer, name='answer'),
        ]