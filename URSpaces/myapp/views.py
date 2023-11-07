from django.shortcuts import render, HttpResponse

# Create your views here.
def login(request):
    return render(request, "login.html")

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

def signup(request):
    return render(request, "signup.html")

def user(request):
    return render(request, "user.html")

def subforum(request):
    return render(request, "subforum.html")