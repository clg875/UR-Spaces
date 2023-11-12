from django.contrib import admin
from .models import Posts, Comment, Moderator, Student , SubForum
from django.contrib.auth.models import User
# Register your models here.

#admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Comment)
admin.site.register(Moderator)
admin.site.register(Student)
admin.site.register(SubForum)

