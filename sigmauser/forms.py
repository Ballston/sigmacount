from django import forms
from sigmauser.models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields = ('username', 'email', 'password')
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields={'description', 'organisation', 'website', 'picture'}
        
class UserLoginForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username','password')


