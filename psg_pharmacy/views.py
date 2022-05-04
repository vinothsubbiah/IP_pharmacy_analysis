from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.http import HttpResponse
from django.urls import reverse
from .models import Messages




def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        role = request.POST['role']

        if(pass1==pass2):
            Myuser = User.objects.create_user(username,pass1,role)
            Myuser.save()
            messages.success(request,'Account created!')
            return redirect("signin")

    return render(request, "signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password']

        user = authenticate(username=username,password=pass1)
        print(user)
        if user is not None:
            #print("1")
            login(request,user)
            name = user.username
            role = user.email
            print(role)
            print("BATMAN!!")
            return render(request, 'index.html', {'username': name})

        else:
            #print("2")
            messages.error(request, 'Bad credentaials')

            return redirect('signin')
    #print("3")
    return render(request, "login.html")

def dashboard(request):
    if request.user.is_authenticated:
        name = request.user.username
        return render(request,'dashboard.html', {'username': name})
    else:
        return render(request, "login.html")
        

def index(request):
    if request.user.is_authenticated:
        name = request.user.username
        return render(request, "index.html", {'username': name})
    else:
        return render(request, "login.html")

def details(request):
    if request.user.is_authenticated:
        name = request.user.username
        return render(request,'details.html', {'username': name})
    else:
        return render(request, "login.html")
    

def alerts(request):
    if request.user.is_authenticated:
        name = request.user.username
        return render(request, 'alerts.html', {'username': name})
    else:
        return render(request, "login.html")
    

def requests(request):
    if request.user.is_authenticated:
        name = request.user.username
        return render(request, 'requests.html', {'username': name})
    else:
        return render(request, "login.html")
    

def alerts_info(request):
    if request.user.is_authenticated:
        name = request.user.username
        return render(request, 'alerts-info.html', {'username': name})
    else:
        return render(request, "login.html")


def messaiah(request):
    
    if request.user.is_authenticated:
        message = Messages.objects.all()
        for m in message:
            if request.user.username == m.to_user:
                print("its me ",request.user)
                return render(request, "m.html",context={"message" : message})
    else:
        return render(request, "login.html")

    

def signout(request):
    logout(request)
    return render(request, "login.html")