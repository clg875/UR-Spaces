from django.contrib import admin
from .models import Posts, Comments, Likes, Moderator, Student
from django.contrib.auth.models import User
# Register your models here.

#admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Moderator)
admin.site.register(Student)

