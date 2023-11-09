from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from myapp.forms import SignUpForm , UpdateProfileForm , CreateNewPost
from myapp.models import Student , SubForum, Posts, Comment, Like, Moderator 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def help(request):
    return render(request, "help.html")

@login_required
def service(request):
    return render(request, "service.html")

@login_required
def about(request):
    return render(request, "about.html")

@login_required
def index(request):
    sub = SubForum.objects.all()
    return render(request, "index.html", {"indexs": sub})
    #return render(request, "index.html")

@login_required
def posts(request, slug):
    post = get_object_or_404(Posts, slug=slug)
    comments = Comment.objects.filter(Post_ID = post)

    user = request.user
    currentUser = User.objects.get(username = user)
    student = Student.objects.get(User_ID = currentUser)
    if "newComment_form" in request.POST:
        content = request.POST.get("newContents")

        new_comment, created = Comment.objects.get_or_create(User_ID = student, Post_ID = post, com_contents = content)
        

    context = {
        "post":post,
        "comments": comments
    }
    return render(request, "posts.html", context)

#avatar picture is not saving corectly
@login_required
def settings(request):
    user = request.user
    currentUser = User.objects.get(username = user)
    form = UpdateProfileForm(request.POST, request.FILES)
    student = Student.objects.get(User_ID = currentUser)
    if request.method == 'POST':
        if form.is_valid():
            updateProfile = form.save(commit=False)
            bio = form.cleaned_data.get('username')
            updateProfile.pk = student.pk
            updateProfile.User_ID = student.User_ID
            updateProfile.save()
        return redirect("profile")
        
    context = {
        "form": form

    }
    return render(request, "registration/setting.html", context)

#not working correctly yet
@login_required
def profile(request):
    user = request.user
    currentUser = User.objects.get(username = user)
    try:
        student = Student.objects.get(User_ID = currentUser)
        posts = Posts.objects.filter(User_ID = student)
        #student = Student.objects.get(pk = studentObj.pk)
    except:
        student = None
        posts = None

    try:
        moderator = Moderator.objects.get(User_ID = currentUser)
       # moderator = Moderator.objects.get(pk = moderatorObj.pk)
    except:
        moderator = None

    context = {
        "student": student,
        "moderator" : moderator,
        "posts": posts

    }
    return render(request, "profile.html", context)

@login_required
def user(request, slug):
    student= get_object_or_404(Student, slug=slug)
    post = Posts.objects.filter(User_ID = student)
    context = {
        "student": student,
        "post": post
    }
    #added this to check for moderator but should just make the page unaccessable for a moderator
    return render(request, "user.html", context)
 

#error with empty values 
@login_required
def subforum(request, slug):
    forum = get_object_or_404(SubForum, slug=slug)
    post = Posts.objects.filter(SubForum_ID = forum)
    user = request.user
    currentUser = User.objects.get(username = user)
    error = False

   #change this to check for moderator field
    if currentUser.is_staff != True:
        student = Student.objects.get(User_ID = currentUser)

        if "newPost_form" in request.POST:
            header = request.POST.get("newHeader")
            content = request.POST.get("newContents")

            if header is not None and content is not None:
                new_post, created = Posts.objects.get_or_create(User_ID = student, SubForum_ID = forum, post_name = header, contents = content)
            else:
                error = True
    context = {
        "forum": forum,
        "post" : post,
        "error": error

    }
    return render(request, "subforum.html", context)


