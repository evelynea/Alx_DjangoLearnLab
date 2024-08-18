from django.shortcuts import render, redirect

# Create your views here.
from .models import Book
from django.views.generic.detail import DetailView
from .models import Library
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


#role-based access control

def admin_check(user):
    return user.userprofile.role == 'Admin'

def librarian_check(user):
    return user.userprofile.role == 'Librarian'

def member_check(user):
    return user.userprofile.role == 'Member'

@user_passes_test(admin_check)
def Admin_view(request):
    return render(request, 'admin_view.html')

@user_passes_test(librarian_check)
def Librarian_view(request):
    return render(request, 'librarian_view.html')

@user_passes_test(member_check)
def Member_view(request):
    return render(request, 'member_view.html')