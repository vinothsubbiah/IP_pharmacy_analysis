from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.http import HttpResponse
from django.urls import reverse
from .models import Messages,Mail




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
        url1 = "https://app.powerbi.com/reportEmbed?reportId=7b0f05ea-60e4-4f2f-8b1f-422148f528bf&autoAuth=true&ctid=858dc6a1-05e7-48c7-8a2b-4172a00a524a&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWluZGlhLWNlbnRyYWwtYS1wcmltYXJ5LXJlZGlyZWN0LmFuYWx5c2lzLndpbmRvd3MubmV0LyJ9"
        if request.user.first_name == 6:
            return render(request,'dashboard.html', {'username': name, 'url1': url1})
        return render(request,'dashboard.html', {'username': name, 'url1': url1})
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
        message = Messages.objects.all()
        for m in message:
            if request.user.username == "admin":
                print("its me ",request.user)
                return render(request, 'alerts.html', {'username': name,"message" : message})
            elif request.user.username == m.to_user:
                return render(request, 'alerts.html', {'username': name,"message" : message})
            # else:
            #     m.message = "No messages"
            #     print("No messages")
            #     return render(request, 'alerts.html', {'username': name,"message" : message})

    else:
        return render(request, "login.html")
    

def requests(request):
    if request.user.is_authenticated:
        name = request.user.username
        mail = Mail.objects.all()
        for m in mail:
            if request.user.username == "admin":
                print("its me ",request.user)
                return render(request, 'requests.html', {'username': name,"mail" : mail})
            elif request.user.username == m.to_user:
                return render(request, 'requests.html', {'username': name,"mail" : mail})
        
    else:
        return render(request, "login.html")
    
def mailCompose(request):
    if request.user.is_authenticated:
        name = request.user.username
        return render(request, 'mail.html', {'username': name})
    else:
        return render(request, "login.html")
    
def sendMail(request):
    name = request.user.username
    if request.method == "POST":
        my_mail = Mail()
        my_mail.from_user =request.POST['from_user']
        my_mail.to_user = request.POST['to_user']
        my_mail.body = request.POST['body']
        my_mail.save()


    return redirect('requests')

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
    return redirect('signin')