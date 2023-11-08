from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#class User(models.Model):
   # User_ID = models.IntegerField(primary_key=True)
   # user_name = models.CharField(max_length=100)
   # email_address= models.CharField(max_length=100)
  #  password = models.CharField(max_length=50)
   # user_date = models.DateTimeField()

class Posts(models.Model):
    Post_ID = models.IntegerField(primary_key=True)
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    post_name = models.CharField(max_length=250)
    post_sub_name = models.CharField(max_length=250)
    contents = models.CharField(max_length=1500)
    count_likes = models.IntegerField()
    locked = models.BooleanField(default=False)
    pin = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    post_date = models.DateTimeField()
    com_count = models.IntegerField()

class Comments(models.Model):
    Comment_ID = models.IntegerField(primary_key=True)
    Post_ID = models.ForeignKey(Posts, on_delete=models.CASCADE)
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    count_likes = models.IntegerField()
    pin = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    com_contents = models.CharField(max_length=500)
    com_date = models.DateTimeField()

class Likes(models.Model):
    Like_ID = models.IntegerField(primary_key=True)
    Post_ID = models.ForeignKey(Posts, on_delete=models.CASCADE)
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    Comment_ID = models.ForeignKey(Comments, on_delete=models.CASCADE)
    likes = models.IntegerField()


class Moderator(models.Model):
    User_ID = models.OneToOneField(User, on_delete=models.CASCADE)
    Special_P = models.BooleanField(default=True)

class Student(models.Model):
    User_ID = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1500)
    banned = models.BooleanField(default=False)
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)
    reported = models.BooleanField(default=False)

