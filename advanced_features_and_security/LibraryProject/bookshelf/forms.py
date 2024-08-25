from django import forms

class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100, help_text="Enter your name")
    email = forms.EmailField(help_text="Enter your email")
    message = forms.CharField(widget=forms.Textarea, help_text="Enter your message")