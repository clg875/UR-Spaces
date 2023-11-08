from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Use a valid email address.')

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
	

