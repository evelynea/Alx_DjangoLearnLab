from django import forms
from .models import Post, Comment
from taggit.forms import TagWidget

class PostForm(forms.ModelForm):
    tags = TagField(widget=TagWidget())
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': 'Add tags'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['content']
        