from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from myapp.forms import SignUpForm
from myapp.models import Student , SubForums, Posts, Comments, Likes, Moderator 
from django.contrib.auth.models import User



# Create your views here.

def base(request):
    return render(request, "base.html")

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

#def login(request):
      #  return render(request, "registration/login.html")
        ...

def help(request):
    return render(request, "help.html")

def about(request):
    return render(request, "about.html")

def index(request):
    sub = SubForums.objects.all()
    return render(request, "index.html", {"indexs": sub})
    #return render(request, "index.html")

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

def user(request):
    return render(request, "user.html")

#not working yet
def subforum(request):
     if request.method == 'POST':
        selected = request.POST.get('Selected_forum')
        sf = SubForums.objects.get(sub_name = selected)
        try:
            postsIn = Posts.objects.get(SubForum_ID = sf)
        except: 
            postsIn = None
        return render(request, "subforum.html", {'sfor': postsIn, 'forum': sf})
     else:
         return render(request, "subforum.html")

     
    #  if postsIn is not None:
    #     return render(request, "subforum.html", {'sfor': postsIn})
    #  else:
    #      return render(request, "subforum.html", {'sfor': sf})
    # if request.method=='GET':
    #     sku = request.GET.get('value')
    #     postsIn = Posts.objects.get(SubForum_ID = sku)
    #     return render(request, "subforum.html", {'sfor': postsIn})
    
        # if not :
        #     return render(request, 'inventory/product.html')
        # else:
        #     # now you have the value of sku
        #     # so you can continue with the rest
        #     return render(request, 'some_other.html')
     #return render(request, "subforum.html")