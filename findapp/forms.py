from django import forms
from django.contrib.auth.models import User
from .models import BugModel
        
class RegisterForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']   

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class BugForm(forms.ModelForm):
    class Meta:
        model = BugModel
        fields = ['titre', 'bug']