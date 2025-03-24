from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Blogger

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

class BloggerProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(disabled=True)
    
    class Meta:
        model = Blogger
        fields = ['bio', 'profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username
    
    def save(self, commit=True):
        blogger = super().save(commit=False)
        if commit:
            # Update the user's email
            blogger.user.email = self.cleaned_data['email']
            blogger.user.save()
            blogger.save()
        return blogger
