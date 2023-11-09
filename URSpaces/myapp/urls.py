from django.urls import path
from .views import signin, help, about, index, posts, service, settings, signupPage, user, subforum 

urlpatterns = [
    #path("base.html", views.base, name="base"),
    path("login/", signin, name="login"),
    path("", signin, name="login"),
    path("help/", help, name="help"),
    path("about/", about, name="about"),
    path("index/", index, name="index"),
    path("posts/", posts, name="posts"),
    path("service/", service, name="service"),
    path("setting/", settings, name="setting"),
    path("signup/", signupPage, name="signup"),
    path("user/", user, name="user"),
    path("subforum/<slug>/", subforum, name="subforum")
    #path("login.html", views.signIn, name="signIn")

]