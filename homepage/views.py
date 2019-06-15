from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    params = {
            'title': 'wattaihei page',
            'msg': 'This is homepage created by wattaihei',
            }
    return render(request, 'homepage/index.html', params)