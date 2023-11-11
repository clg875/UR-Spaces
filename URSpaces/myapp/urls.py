from django.contrib import admin
from django.urls import path
from .views import signin, help, about, index, posts, service, settings, signupPage, user, subforum, profile, report

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("login/", signin, name="login"),
    path("", signin, name="login"),
    path("help/", help, name="help"),
    path("about/", about, name="about"),
    path("index/", index, name="index"),
    path("posts/<slug>/", posts, name="posts"),
    path('posts/<slug>/<pk>/', posts, name='comment_update'),
    path("service/", service, name="service"),
    path("setting/", settings, name="setting"),
    path("signup/", signupPage, name="signup"),
    path("user/<slug>/", user, name="user"),
    path("profile/", profile, name="profile"),
    path("subforum/<slug>/", subforum, name="subforum"),
    path("report/", report, name="report"),
     path('report/<pk>/', report, name='report_update'),

]
