from django.contrib.auth import views as auth_views

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.db import models

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post

class LoginView(auth_views.LoginView):
    template_name = 'auth/login.html'

class LogoutView(auth_views.LogoutView):
    template_name = 'auth/logged_out.html'


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2'
        ]
    
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        # Handle profile update logic here
        pass
    return render(request, 'auth/profile.html')

# ListView - Display all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']  #Optional: Order by most recent posts


#DetailView -Display a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


#CreateView - Allow authenticated users to creaet a post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    form_class = PostForm


    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author to the current logged-in user
        return super().form_valid(form)
    
#UpdateView - Allow post author to update the post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
# DeleteView - Allow post author to delete the post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-list')
    template_name = 'blog/post_confirm_delete.html'


    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author