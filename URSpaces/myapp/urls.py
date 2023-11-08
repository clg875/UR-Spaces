from django.urls import path
from . import views

urlpatterns = [
    path("base.html", views.base, name="base"),
    path("login.html", views.signin, name="login"),
    path("", views.signin, name="login"),
    path("help.html", views.help, name="help"),
    path("about.html", views.about, name="about"),
    path("index.html", views.index, name="index"),
    path("posts.html", views.posts, name="posts"),
    path("service.html", views.service, name="service"),
    path("setting.html", views.settings, name="setting"),
    path("signup.html", views.signupPage, name="signup"),
    path("user.html", views.user, name="user"),
    path("subforum.html", views.subforum, name="subforum")
    #path("login.html", views.signIn, name="signIn")

]