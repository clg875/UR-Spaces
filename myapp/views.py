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


#Login function
# Displays login.html
#Processes the username and password entered by the user 
#Redirects to the index page if login is sucessful or displays an error message if not
#Does not allow login if the Student has been banned and displays a message saying so 
def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    user = authenticate(request, username=username, password=password)
    banned = False
    er = False
    
    if user is not None:
    
        currentUser = User.objects.get(username = user)
        try:
            student = Student.objects.get(User_ID = currentUser)
        except:
            student = None

        if student is not None:
            if student.banned == False:
                login(request, user)
                return redirect('index')
            else:
                banned = True
                return render(request, "registration/login.html", {"error": er, "banned": banned})
        else:
            login(request, user)
            return redirect('index')

    else:
        if username is not None and password is not None:
            er = True
        return render(request, "registration/login.html", {"error": er, "banned": banned})


#Signup function
# Displays signup.html 
#Processes the username, email, password, and confirmed password entered by the user 
#Redirects to the login page if sign up is sucessful or displays an error message if not  
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
            new_student = Student()
            new_student.User_ID = User.objects.get(username = username)
            new_student.bio = "Please add bio"
            new_student.slug = slugify(username)
            new_student.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

#Report function
#Displays report.html with all student, post and comments that have been reported by students
#Processes banning the user if a ban button has been pressed by the moderator
#Processes ignoring the report if an ignore button has been pressed by the moderator
#Redirects to report page after any processes 
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

#Help function
#Displays help.html
@login_required
def help(request):
    return render(request, "help.html")

#Service function
#Displays service.html
@login_required
def service(request):
    return render(request, "service.html")

#About function
#Displays about.html
@login_required
def about(request):
    return render(request, "about.html")

#Index function
#Displays the homepage index.html with all the existing Subforums
#Processes a subforum being clicked 
#Redirects to clicked subforum page
@login_required
def index(request):
    sub = SubForum.objects.all()
    return render(request, "index.html", {"indexs": sub})


#Posts function
#Displays posts.html with post and any comments related to the post
#Processes deleting a comment or post if the corresponding button has been pressed
#Processes locking and unlocking a post if the corresponding button has been pressed by the moderator
#Processes adding and editing a comment if the corresponding field on the page has been filled out by a student
#Processes reporting the post or comment if the corresponding button has been pressed by the student
#Processes editing a post if the corresponding field on the page has been filled out by a student
#Redirects to the same post page unless the post is deleted, then it redirects to the subforum page
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
        firstCommentId = comments[0].pk

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
                CommentId = comments[0].pk
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
            redirect_url = reverse('posts', args=[slug])
            return redirect(redirect_url)


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
                CommentId = comments[0].pk
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

#Setting function
#Displays setting.html 
#Processes changing a students bio if the corresponding field on the page has been filled out by a student
#Redirects to the student's profile page
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
            updateProfile.banned = student.banned
            updateProfile.reported = student.reported
            updateProfile.save()
        return redirect("profile")
        
    context = {
        "form": form

    }
    return render(request, "registration/setting.html", context)

#Profile function
#Displays profile.html with the student's bio and any posts the student has made or a message about moderator accounts
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

#Profile function
#Displays profile.html with the selected student's bio and any posts the student has made 
#Processes reporting the student if the corresponding button has been pressed by the current student
#Redirects to the same user page after processes
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
 

#Subforum function
#Displays subfroum.html with posts in that subforum
#Processes pinning and unpinning a post if the corresponding button has been pressed by the moderator
#Processes adding a post if the corresponding field on the page has been filled out by a student
#Redirects to the same subforum page after processes
@login_required
def subforum(request, slug, pk=None):
    forum = get_object_or_404(SubForum, slug=slug)
    post = Posts.objects.filter(SubForum_ID = forum, User_ID__banned =False)
    pinnedPosts = Posts.objects.filter(SubForum_ID = forum, User_ID__banned =False, pin =True)
    unpinnedPosts = Posts.objects.filter(SubForum_ID = forum, User_ID__banned =False, pin =False)
    user = request.user
    currentUser = User.objects.get(username = user)
    error = False

    if post.exists():
        if pk:
            updatePost = post.get(pk = pk)
            if "pinPost" in request.POST:
                pinPost = Posts.objects.get(pk = pk)
                pinPost.User_ID = updatePost.User_ID
                pinPost.SubForum_ID = forum
                pinPost.post_name =updatePost.post_name
                pinPost.contents =updatePost.contents
                pinPost.post_date =updatePost.post_date
                pinPost.count_likes = updatePost.count_likes
                pinPost.reported = updatePost.reported
                pinPost.pin = True
                pinPost.locked = updatePost.locked
                pinPost.slug = updatePost.slug
                pinPost.save()
                pinnedPosts = Posts.objects.filter(SubForum_ID = forum, User_ID__banned =False, pin =True)
                unpinnedPosts = Posts.objects.filter(SubForum_ID = forum, User_ID__banned =False, pin =False)

            if "unpinPost" in request.POST:
                pinPost = Posts.objects.get(pk = pk)
                pinPost.User_ID = updatePost.User_ID
                pinPost.SubForum_ID = forum
                pinPost.post_name =updatePost.post_name
                pinPost.contents =updatePost.contents
                pinPost.post_date =updatePost.post_date
                pinPost.count_likes = updatePost.count_likes
                pinPost.reported = updatePost.reported
                pinPost.pin = False
                pinPost.locked = updatePost.locked
                pinPost.slug = updatePost.slug
                pinPost.save()
                pinnedPosts = Posts.objects.filter(SubForum_ID = forum, User_ID__banned =False, pin =True)
                unpinnedPosts = Posts.objects.filter(SubForum_ID = forum, User_ID__banned =False, pin =False)
    
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
        "pinnedPosts": pinnedPosts,
        "unpinnedPosts": unpinnedPosts,

    }
    return render(request, "subforum.html", context)

#PostLike function
#Subject view for Likes on Posts
#Keeps track of updates to likes and redirects to the subforum page when updated.

def PostLike(request, pk):
    post = get_object_or_404(Posts, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    redirect_url = reverse('subforum', args=[post.SubForum_ID.slug])
    return redirect(redirect_url)

#CommentLike function
#Subject view for Likes on Comments
#Keeps track of updates to likes and redirects to the post page when updated.
def CommentLike(request, pk):
    post = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    redirect_url = reverse('posts', args=[post.Post_ID.slug])
    return redirect(redirect_url)

#PostDetailView function
#Observer view for Likes on Posts
#Passes information on total likes to the observer webpage
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

#CommentDetailView function
#Observer view for Likes on Comments
#Passes information on total likes to the observer
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

