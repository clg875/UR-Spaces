from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.urls import reverse


# Create your models here.

class Moderator(models.Model):
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    Special_P = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.User_ID}"

class Student(models.Model):
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(default="Please add bio in settings", blank=True)
    banned = models.BooleanField(default=False)
    avatar =ResizedImageField(size=[50, 80], quality=100, upload_to="authors", default=None, null=True, blank=True)
    reported = models.BooleanField(default=False)
    slug = models.SlugField(max_length=400, unique=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.User_ID)
    #         super(Student, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("user", kwargs={
            "slug":self.slug
        })
    
    def __str__(self):
        return f"{self.User_ID} {self.bio}"

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
    
    def __str__(self):
        return f"{self.sub_name}"

    @property
    def num_posts(self):
        return Posts.objects.filter(SubForum_ID = self, User_ID__banned =False).count()
    


class Posts(models.Model):
    User_ID = models.ForeignKey(Student, on_delete=models.CASCADE)
    SubForum_ID = models.ForeignKey(SubForum, default= 1, on_delete=models.CASCADE)
    post_name = models.TextField(max_length=400)
    contents = models.TextField()
    count_likes = models.IntegerField(default=0, blank=True, )
    locked = models.BooleanField(default=False)
    pin = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    post_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=400, unique=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.post_name)
    #         super(Posts, self).save(*args, **kwargs)
    
    def get_url(self):
        return reverse("posts", kwargs={
            "slug":self.slug
        })
    
    def __str__(self):
        return f"{self.User_ID} {self.SubForum_ID} {self.post_name} {self.post_date}"
    
    @property
    def num_comments(self):
        return Comment.objects.filter(Post_ID = self, User_ID__banned =False).count()
    
class Comment(models.Model):
    #Comment_ID = models.IntegerField(primary_key=True)
    Post_ID = models.ForeignKey(Posts, on_delete=models.CASCADE)
    User_ID = models.ForeignKey(Student, on_delete=models.CASCADE)
    count_likes = models.IntegerField(default=0)
    pin = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    com_contents = models.TextField(max_length=500)
    com_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Post_ID} {self.User_ID}"

class Like(models.Model):
    #Like_ID = models.IntegerField(primary_key=True)
    Post_ID = models.ForeignKey(Posts, on_delete=models.CASCADE)
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    Comment_ID = models.ForeignKey(Comment, on_delete=models.CASCADE)
    likes_count = models.IntegerField()

    def __str__(self):
        return f"{self.Post_ID} {self.User_ID}"




