from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from myapp.forms import SignUpForm #, CreateNewPost
from myapp.models import Student , SubForum, Posts, Comment, Like, Moderator 
from django.contrib.auth.models import User



# Create your views here.

def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')
        # return render(request, "index.html")
        ...
    else:
        er = False
        if username is not None and password is not None:
            er = True
        return render(request, "registration/login.html", {"error": er})
    
def signupPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            account = User.objects.get(username = username)
            account.email = email
            account.save()
            #raw_password = form.cleaned_data.get('password')
            #user = authenticate(username=username, password=raw_password)
            new_student = Student()
            new_student.User_ID = User.objects.get(username = username)
            new_student.bio = "Please add bio"
            new_student.save()
            #login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

#def login(request):
#  return render(request, "registration/login.html")

def help(request):
    return render(request, "help.html")

def about(request):
    return render(request, "about.html")

def index(request):
    sub = SubForum.objects.all()
    return render(request, "index.html", {"indexs": sub})
    #return render(request, "index.html")

def posts(request, slug):
    post = get_object_or_404(Posts, slug=slug)
    comments = Comment.objects.filter(Post_ID = post)
    context = {
        "post":post,
        "comments": comments
    }
    return render(request, "posts.html", context)

def service(request):
    return render(request, "service.html")

def settings(request):
    return render(request, "setting.html")

#not working correctly yet
def profile(request):
    user = request.user.username
    currentUser = User.objects.get(username = user)
    # try:
    student = Student.objects.filter(User_ID = currentUser)
    moderator = Moderator.objects.filter(User_ID = currentUser)
    # except:
    #     student = None
    #     moderator = None
    context = {
        "student": student,
        "moderator" : moderator

    }
    return render(request, "profile.html", context)

def user(request, slug):
    student= get_object_or_404(Student, slug=slug)
    post = Posts.objects.filter(User_ID = student)
    context = {
        "student": student,
        "post": post
    }
    #added this to check for moderator but should just make the page unaccessable for a moderator
    return render(request, "user.html", context)
 

def subforum(request, slug):
    forum = get_object_or_404(SubForum, slug=slug)
    post = Posts.objects.filter(SubForum_ID = forum)

    context = {
        "forum": forum,
        "post" : post

    }
    return render(request, "subforum.html", context)


