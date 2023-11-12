from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from myapp.forms import SignUpForm , UpdateProfileForm , CreateNewPost , UpdatePostForm, UpdateCommentForm, ReportPostForm#, DeletePostForm
from myapp.models import Student , SubForum, Posts, Comment, Like, Moderator 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from datetime import datetime
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic.detail import DetailView

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
            new_student.slug = slugify(username)
            new_student.save()
            #login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def report(request, pk=None):
    students = Student.objects.filter(reported=True, banned=False)
    posts = Posts.objects.filter(reported=True, User_ID__banned =False)
    comments = Comment.objects.filter(reported=True, User_ID__banned =False)

    if "banUser_btn" in request.POST:
        banUser = Student.objects.get(pk=pk)
        banUser.banned = True
        banUser.save()
        return redirect("report")
    
    if "ignoreUser_btn" in request.POST:
        ignoreUser = Student.objects.get(pk=pk)
        ignoreUser.reported = False
        ignoreUser.save()
        return redirect("report")


    if "banUserPost_btn" in request.POST:
        postUser = Posts.objects.get(pk=pk)
        banUser = Student.objects.get(pk= postUser.User_ID.pk)
        banUser.banned = True
        banUser.save()
        return redirect("report")
    
    if "ignorePost_btn" in request.POST:
        ignorePost = Posts.objects.get(pk=pk)
        ignorePost.reported = False
        ignorePost.save()
        return redirect("report")
    
    if "banUserComment_btn" in request.POST:
        commentUser = Comment.objects.get(pk=pk)
        banUser = Student.objects.get(pk = commentUser.User_ID.pk)
        banUser.banned = True
        banUser.save()
        return redirect("report")
    
    if "ignoreComment_btn" in request.POST:
        ignoreComment = Comment.objects.get(pk=pk)
        ignoreComment.reported = False
        ignoreComment.save()
        return redirect("report")


    context = {
        "students": students,
        "posts":posts,
        "comments": comments,

    }



    return render(request, "report.html", context)

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
def posts(request, slug, pk =None):
    post = get_object_or_404(Posts, slug=slug)
    comments = Comment.objects.filter(Post_ID = post, User_ID__banned =False)
    forum = SubForum.objects.get(pk = post.SubForum_ID.pk)
    user = request.user
    currentUser = User.objects.get(username = user)
    error = False
    form = UpdatePostForm(request.POST)

    if comments.exists():
        firstCommentId = comments[0].id

        if pk:
            commentform = UpdateCommentForm(instance=Comment.objects.get(pk=pk), data=request.POST)
        else:
            commentform = UpdateCommentForm(instance=Comment.objects.get(pk=comments[0].pk), data=request.POST)
    else:
        firstCommentId = 0
        commentform = None

    try:
        moderator = Moderator.objects.get(User_ID = currentUser)
    except:
        moderator = None

    context = {
        "post":post,
        "comments": comments,
        "error": error,
        "form": form,
        "commentform":commentform,
        "moderator": moderator,
        "firstCommentId": firstCommentId,

    }

    if "deleteComment_btn" in request.POST:
            if comments.exists() and pk is None:
                CommentId = comments[0].id
            else:
                CommentId = pk
            deleteComment = Comment.objects.get(pk = CommentId)
            deleteComment.Post_ID = post 
            deleteComment.User_ID = post.User_ID
            deleteComment.delete()
            redirect_url = reverse('posts', args=[slug])
            return redirect(redirect_url)
    
    if "deletePost_btn" in request.POST:
            deletePost = Posts.objects.get(pk = post.pk)
            deletePost.User_ID = post.User_ID
            deletePost.SubForum_ID = forum
            deletePost.delete()
            redirect_url = reverse('subforum', args=[forum.slug])
            return redirect(redirect_url)
    
    if "lockPost_btn" in request.POST:
            lockPost = Posts.objects.get(pk = post.pk)
            lockPost.pk = post.pk
            lockPost.User_ID = post.User_ID
            lockPost.SubForum_ID = forum
            lockPost.post_name =post.post_name
            lockPost.contents =post.contents
            lockPost.post_date =post.post_date
            lockPost.count_likes = post.count_likes
            lockPost.reported = post.reported
            lockPost.pin = post.pin
            lockPost.locked = True
            lockPost.slug = post.slug  
            lockPost.save()
            redirect_url = reverse('subforum', args=[forum.slug])
            return redirect(redirect_url)
    
    if "unlockPost_btn" in request.POST:
            unlockPost = Posts.objects.get(pk = post.pk)
            unlockPost.pk = post.pk
            unlockPost.User_ID = post.User_ID
            unlockPost.SubForum_ID = forum
            unlockPost.post_name =post.post_name
            unlockPost.contents =post.contents
            unlockPost.post_date =post.post_date
            unlockPost.count_likes = post.count_likes
            unlockPost.reported = post.reported
            unlockPost.pin = post.pin
            unlockPost.locked = False
            unlockPost.slug = post.slug  
            unlockPost.save()
            redirect_url = reverse('subforum', args=[forum.slug])
            return redirect(redirect_url)

    if moderator is None:
        
        student = Student.objects.get(User_ID = currentUser)

        if "newComment_form" in request.POST:
            content = request.POST.get("newCommentContents")

            new_comment, created = Comment.objects.get_or_create(User_ID = student, Post_ID = post, com_contents = content)


        if "editComment_form" in request.POST:
            updateComment = commentform.save(commit=False)
            updateComment.Post_ID = post 
            updateComment.User_ID = student
            updateComment.com_date = datetime.now()
            updateComment.save()
            redirect_url = reverse('posts', args=[slug])
            return redirect(redirect_url)

        if "reportComment_btn" in request.POST:
            if comments.exists() and pk is None:
                CommentId = comments[0].id
            else:
                CommentId = pk
            reportComment = Comment.objects.get(pk = CommentId)
            reportComment.reported = True
            reportComment.save()
            redirect_url = reverse('posts', args=[slug])
            return redirect(redirect_url)
        
        if "reportPost_btn" in request.POST:
            reportPost = Posts.objects.get(pk = post.pk)
            reportPost.pk = post.pk
            reportPost.User_ID = post.User_ID
            reportPost.SubForum_ID = forum
            reportPost.post_name =post.post_name
            reportPost.contents =post.contents
            reportPost.post_date =post.post_date
            reportPost.count_likes = post.count_likes
            reportPost.reported = True
            reportPost.pin = post.pin
            reportPost.locked = post.locked
            reportPost.slug = post.slug               
            reportPost.save()
            post = Posts.objects.get(pk = reportPost.pk)

            context2 = {
                    "post":post,
                    "comments": comments,
                    "error": error,
                    "form": form,
                    "commentform":commentform,
                    "moderator": moderator,
                    "firstCommentId": firstCommentId,
            }
            return render(request, "posts.html", context2)

        if "editPost_form" in request.POST:
            
            if form.is_valid():
                updatePost = form.save(commit=False)
                updatePost.pk = post.pk 
                updatePost.User_ID = student
                updatePost.SubForum_ID = forum
                updatePost.post_name = post.post_name
                updatePost.slug = post.slug
                updatePost.reported =post.reported
                updatePost.post_date = datetime.now()
                updatePost.save()

                post = Posts.objects.get(pk = updatePost.pk)

                context2 = {
                    "post":post,
                    "comments": comments,
                    "error": error,
                    "form": form,
                    "commentform":commentform,
                    "moderator": moderator,
                    "firstCommentId": firstCommentId,
                }
                return render(request, "posts.html", context2)
            
            
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
            updateProfile.slug =student.slug
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
    user = request.user
    currentUser = User.objects.get(username = user)

    try:
        moderator = Moderator.objects.get(User_ID = currentUser)
    except:
        moderator = None

    if "reportUser_btn" in request.POST:
        reportStudent = Student.objects.get(pk = student.pk)
        reportStudent.User_ID = student.User_ID
        reportStudent.bio = student.bio
        reportStudent.avatar = student.avatar
        reportStudent.banned = student.banned
        reportStudent.slug = student.slug
        reportStudent.reported = True
        reportStudent.save()

        student = Student.objects.get(pk = reportStudent.pk)



    context = {
        "student": student,
        "post": post,
        "moderator": moderator
    }

    return render(request, "user.html", context)
 

#error with empty values 
@login_required
def subforum(request, slug):
    forum = get_object_or_404(SubForum, slug=slug)
    post = Posts.objects.filter(SubForum_ID = forum, User_ID__banned =False)
    user = request.user
    currentUser = User.objects.get(username = user)
    error = False

    try:
        moderator = Moderator.objects.get(User_ID = currentUser)
    except:
        moderator = None

    if moderator is None:
        student = Student.objects.get(User_ID = currentUser)

        if "newPost_form" in request.POST:
            header = request.POST.get("newHeader")
            content = request.POST.get("newContents")

            if header != "" and content != "":
                new_post, created = Posts.objects.get_or_create(User_ID = student, SubForum_ID = forum, post_name = header, contents = content, slug = slugify(header)+get_random_string(5))
            else:
                error = True
    context = {
        "forum": forum,
        "post" : post,
        "error": error,
        "moderator": moderator,

    }
    return render(request, "subforum.html", context)

def PostLike(request, pk):
    post = get_object_or_404(Posts, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    redirect_url = reverse('subforum', args=[post.SubForum_ID.slug])
    return redirect(redirect_url)

def CommentLike(request, pk):
    post = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    redirect_url = reverse('posts', args=[post.Post_ID.slug])
    return redirect(redirect_url)


class PostDetailView(DetailView):
    model = Posts
    #template_name = subforum.html
    # context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stuff = get_object_or_404(Posts, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        return context
    
class CommentDetailView(DetailView):
    model = Comment
    # template_name = MainApp/BlogPost_detail.html
    # context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stuff = get_object_or_404(Comment, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        return context

