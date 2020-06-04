from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
    """Form to be used to log users in"""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
    """Form used to register a new user"""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation", 
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        help_texts = {
            'username': None,
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'This email address is already in use. Please use a unique email address.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'This username already exists. Please choose a unique username.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if len(password1) < 6:
            raise ValidationError("Password must be at least 6 characters.")

        if not password1 or not password2:
            raise ValidationError("Please confirm your password")

        if password1 != password2:
            raise ValidationError("Passwords must match")

        return password2

class EditProfileForm(UserChangeForm):
    """Form to be used to edit profile details"""
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']