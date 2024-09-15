from django.contrib.auth import views as auth_views

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.db import models

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CommentForm

from django.db.models import Q
from taggit.models import Tag

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
    context_object_name ='post'

    def get_context_data(self, **kwargs):
        context = super().get_context_dat(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)  # Fetch comments related to the post
        context['form'] = CommentForm()  # Initialize an empty form for adding comments
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=self.object.pk)
        return self.get(request, *args, **kwargs)  # Re-render the page if form is invalid

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
    
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('post_detail', pk=self.kwargs['post_id'])  # Redirect back to the post after a successful comment

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Ensure the user is the comment author
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('post_list')  # Redirect to the post list or post detail page after deletion

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Only allow the comment author to delete
    


def Post_search(request):
    query = request.GET.get('q')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})

def PostsByTagListView(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])

    return render(request, 'blog/posts_by_tag.html', {'posts': posts, 'tag': tag})