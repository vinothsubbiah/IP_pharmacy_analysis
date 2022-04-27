from django.shortcuts import render
from django.http import HttpResponse


def dashboard(request):
    return render(request,'dashboard.html')
# Create your views here.
def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')

def details(request):
    return render(request, 'details.html')

def alerts(request):
    return render(request, 'alerts.html')

def requests(request):
    return render(request, 'requests.html')

def alerts_info(request):
    return render(request, 'alerts-info.html')