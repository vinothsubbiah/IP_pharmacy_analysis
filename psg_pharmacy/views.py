from django.shortcuts import render
from django.http import HttpResponse
from . import views

def dashboard(request):
    return render(request,'dashboard.html')
# Create your views here.
