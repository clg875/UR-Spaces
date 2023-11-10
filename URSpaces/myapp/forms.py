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
        fields = ("avatar", "bio" )

class UpdatePostForm(forms.ModelForm):

    
    class Meta:
        model = Posts
        fields = ("contents", )


class CreateNewPost(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ("post_name", "contents" )

# class SelectSubForum(forms.Form):
#     selectedForum = forms.CharField(max_length=100)

    # class Meta:
    #     model = User
    #     fields = ('username', 'email', 'password1', 'password2', )


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


# # Create your forms here.

# class NewUserForm(UserCreationForm):
# 	email = forms.EmailField(required=True)

# 	class Meta:
# 		model = User
# 		fields = ("username", "email", "password1", "password2")

# 	def save(self, commit=True):
# 		user = super(NewUserForm, self).save(commit=False)
# 		user.email = self.cleaned_data['email']
# 		if commit:
# 			user.save()
			
# 		return user
	

