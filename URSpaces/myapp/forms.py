from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myapp.models import Student, Posts, Comment


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Use a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2' )

class UpdateProfileForm(forms.ModelForm):

    
    class Meta:
        model = Student
        fields = ("bio", )

class UpdatePostForm(forms.ModelForm):

    
    class Meta:
        model = Posts
        fields = ("contents", )


class ReportPostForm(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ("reported", )

class UpdateCommentForm(forms.ModelForm):

    
    class Meta:
        model = Comment
        fields = ("com_contents", )


class CreateNewPost(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ("post_name", "contents" )


