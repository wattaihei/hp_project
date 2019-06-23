from django.urls import path
from . import views

urlpatterns = [
        path('', views.home, name='home'),
        path('delete', views.delete, name='delete'),
        path('confirm', views.check_delete, name='confirm'),
        path('question/<int:num>', views.question, name='question'),
        path('answer/<int:num>', views.answer, name='answer'),
        ]