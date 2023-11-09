from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.urls import reverse


# Create your models here.

class Moderator(models.Model):
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    Special_P = models.BooleanField(default=True)

class Student(models.Model):
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()
    banned = models.BooleanField(default=False)
    avatar =ResizedImageField(size=[50, 80], quality=100, upload_to="authors", default=None, null=True, blank=True)
    reported = models.BooleanField(default=False)
    slug = models.SlugField(max_length=400, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.User_ID)
            super(Student, self).save(*args, **kwargs)

class SubForum(models.Model):
    sub_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=400, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.sub_name)
            super(SubForum, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("subforum", kwargs={
            "slug":self.slug
        })

class Posts(models.Model):
    User_ID = models.ForeignKey(Student, on_delete=models.CASCADE)
    SubForum_ID = models.ForeignKey(SubForum, default= 1, on_delete=models.CASCADE)
    post_name = models.CharField(max_length=400)
    post_sub_name = models.CharField(max_length=250)
    contents = models.TextField()
    count_likes = models.IntegerField()
    locked = models.BooleanField(default=False)
    pin = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    post_date = models.DateTimeField(auto_now_add=True)
    com_count = models.IntegerField()
    slug = models.SlugField(max_length=400, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.post_name)
            super(Posts, self).save(*args, **kwargs)

class Comment(models.Model):
    #Comment_ID = models.IntegerField(primary_key=True)
    Post_ID = models.ForeignKey(Posts, on_delete=models.CASCADE)
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    count_likes = models.IntegerField()
    pin = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    com_contents = models.CharField(max_length=500)
    com_date = models.DateTimeField()

class Like(models.Model):
    #Like_ID = models.IntegerField(primary_key=True)
    Post_ID = models.ForeignKey(Posts, on_delete=models.CASCADE)
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    Comment_ID = models.ForeignKey(Comment, on_delete=models.CASCADE)
    likes_count = models.IntegerField()




