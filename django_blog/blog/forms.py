from django import forms
from .models import Post, Comment
from taggit.forms import TagWidget

class PostForm(forms.ModelForm):
    widgets = {'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': 'Add tags here'}),}
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['content']
        