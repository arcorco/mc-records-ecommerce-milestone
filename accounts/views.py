from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm, EditProfileForm

# Create your views here.

@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out!")
    return redirect(reverse('home'))

def login(request):
    """Return a login page"""
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have succesfully logged in!")
                return redirect(reverse('profile'))
            else:
                login_form.add_error(None, "Your username or password is incorrect.")

    else:
        login_form = UserLoginForm()
    return render(request, "login.html", {"login_form": login_form})

def registration(request):
    """Render the registration page"""
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered")
                return redirect(reverse('profile'))

            else:
                messages.error(request, "Unable to register your account at this time")
    
    else:
        registration_form = UserRegistrationForm()

    return render(request, "register.html", {
        "registration_form": registration_form})

def user_profile(request):
    """The user's profile page"""
    user = User.objects.get(email=request.user.email)
    return render(request, "profile.html", {
        "profile": user
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        edit_form = EditProfileForm(request.POST, instance=request.user)

        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "You have successfully updated your details!")
            return redirect(reverse('profile'))

    else:
        edit_form = EditProfileForm(instance=request.user)
        args = {'edit_form': edit_form}
        return render(request, "edit_profile.html", args)

            

