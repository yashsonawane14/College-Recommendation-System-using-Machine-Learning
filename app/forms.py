from django import forms

class RecommendationForm(forms.Form):
    rank = forms.IntegerField(label='Rank')
    percentile = forms.FloatField(label='Percentile')
    category = forms.CharField(label='Category')
    gender = forms.CharField(label='Gender')
    branch = forms.CharField(label='Branch')  # Add this field for user input


    
# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']