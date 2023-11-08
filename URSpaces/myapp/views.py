from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from myapp.forms import SignUpForm
from .models import Posts, Comments, Likes, Moderator, Student
from django.contrib.auth.models import User



# Create your views here.

def base(request):
    return render(request, "base.html")

def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        #(request, "registration/login.html")
        login(request, user)
        # Redirect to a success page.
        return render(request, "index.html")
        ...
    else:
        # Return an 'invalid login' error message.
        return render(request, "registration/login.html")

#def login(request):
      #  return render(request, "registration/login.html")
        ...

def help(request):
    return render(request, "help.html")

def about(request):
    return render(request, "about.html")

def index(request):
    return render(request, "index.html")

def posts(request):
    return render(request, "posts.html")

def service(request):
    return render(request, "service.html")

def settings(request):
    return render(request, "setting.html")

#def signup(request):
    #return render(request, "signup.html")

def signupPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            new_student = Student(User_ID = username)
            new_student.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user(request):
    return render(request, "user.html")

def subforum(request):
    return render(request, "subforum.html")