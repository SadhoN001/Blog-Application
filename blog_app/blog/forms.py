from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Tag, Post, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'featured_img', 'tags']
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

        
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required= True)
    class Meta:
        model =  User
        fields = ['username', 'email', 'password1', 'password2']