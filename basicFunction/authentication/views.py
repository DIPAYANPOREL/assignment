from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils.timezone import now


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
        else:
            if 'username' in form.errors:
                messages.error(request, form.errors['username'][0])
            if 'email' in form.errors:
                messages.error(request, form.errors['email'][0])
            if 'password' in form.errors:
                messages.error(request, form.errors['password'][0])
            if 'confirm_password' in form.errors:
                messages.error(request, form.errors['confirm_password'][0])
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Get username/email from form
        password = request.POST.get('password')
        
        print(f"Login attempt - Username/Email: {username}")  # Debug print
        
        # First try to authenticate with username
        user = authenticate(request, username=username, password=password)
        
        # If that fails, try to find user by email
        if user is None:
            try:
                user_obj = CustomUser.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                user = None
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            print(f"User authenticated successfully: {user.username}")  # Debug print
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username/email or password.')
            print("Authentication failed - Invalid credentials")  # Debug print
            
    return render(request, 'authentication/login.html')

@login_required
def profile(request):
    user = request.user
    # Set the last profile update time if it's a profile edit view
    user.last_profile_update = now()
    user.save(update_fields=['last_profile_update'])
    
    context = {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined.strftime("%Y-%m-%d"),
        'last_profile_update': user.last_profile_update.strftime("%Y-%m-%d %H:%M:%S") if user.last_profile_update else "Never",
    }
    return render(request, 'authentication/profile.html', context)


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login') 

@login_required  # Ensure the user is logged in to access the home page
def home(request):
    return render(request, 'authentication/home.html', {'user': request.user})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Check if the new password is the same as the old password
            if form.cleaned_data['new_password1'] == form.cleaned_data['old_password']:
                messages.error(request, 'The new password cannot be the same as the old password.')
                return render(request, 'authentication/change_password.html', {'form': form, 'user': request.user})

            # Save the new password
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'authentication/change_password.html', {
        'form': form,
        'user': request.user
    })

