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
# temp
 
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print(form.errors)
        print('outside')
        if form.is_valid():
            user = form.save()
            print('hi')

            # Check the role
            role = request.POST.get('role')
            if role == 'instructor':
                instructor_name = request.POST.get('instructorName')
                instructor_qualification = request.POST.get('instructorQualification')

                # Save instructor data
                InstructorData.objects.create(
                    user=user,
                    instructorName=instructor_name,
                    instructorQualification=instructor_qualification
                )

            # Authenticate the user before logging in
            user = authenticate(username=user.username, password=request.POST.get('password1'))

            if user is not None:
                # Log the user in and redirect to home
                # login(request, user)  # Call the correct login function with request and user
                return redirect('home')  # Make sure you have 'home' URL defined in urls.py
    else:
        form = SignUpForm()

    return render(request, 'login/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # login(request, user)
                return redirect('dashboard')  # Redirect to dashboard or another page after successful login
            else:
                messages.error(request, 'Invalid username or password')
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