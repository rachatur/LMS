from pyexpat.errors import messages

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import user_passes_test
from .forms import SignUpForm, LoginForm
from .models import InstructorData
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login
from django.contrib.auth import login as auth_login


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create the user object but don't save it yet
            user = form.save(commit=False)

            # Set the password manually
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()

            # Handle role-specific data
            role = request.POST.get('role')
            if role == 'instructor':
                instructor_name = request.POST.get('instructorName')
                instructor_qualification = request.POST.get('instructorQualification')

                # Save the instructor-specific data
                InstructorData.objects.create(
                    user=user,
                    instructorName=instructor_name,
                    instructorQualification=instructor_qualification
                )

            # Authenticate the user
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user is not None:
                # Log the user in if authentication is successful
                login(request, authenticated_user)
                return redirect('dashboard')  # Ensure 'home' is defined in your URLs
            else:
                # Handle the case where authentication fails (unlikely but good practice)
                print("Authentication failed")
        else:
            # Print form errors if the form is invalid
            print("Form is not valid", form.errors)
    else:
        form = SignUpForm()

    return render(request, 'login/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Log in the user if authentication is successful
                auth_login(request, user)  # Use the renamed login
                return redirect('dashboard')  # Redirect to the dashboard after logging in
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})


def reset_password_view(request):
    User = get_user_model()  # Use the custom user model
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after changing password
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('login')  # Redirect to login page after success
        except User.DoesNotExist:
            messages.error(request, 'User not found. Please enter a valid username.')

    return render(request, 'login/reset_password.html')


def dashboard(request):
    return render(request, 'courses_details/dashboard.html')


def home(request):
    return render(request, 'courses_details/home.html')

def my_courses(request):
    return render(request, 'courses_details/my_courses.html')

def course_store(request):
    return render(request, 'courses_details/course_store.html')

def instructor(request):
    return render(request, 'courses_details/instructor.html')

def contact_us(request):
    return render(request, 'courses_details/contact_us.html')

def about_us(request):
    return render(request, 'courses_details/about_us.html')

def login(request):
    return render(request, 'courses_details/login.html')

def profile(request):
    return render(request, 'courses_details/profile.html')

def admin(request):
    return render(request, 'courses_details/admin.html')