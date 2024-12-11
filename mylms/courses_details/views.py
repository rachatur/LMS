from django.urls import reverse
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import Http404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login as auth_login
from .forms import *
from .models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import IntegrityError
from .models import Group, User
from django.contrib.auth import get_user_model


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
                auth_login(request, authenticated_user)
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

            # Get the custom user model
            User = get_user_model()

            # Check if the user exists
            user = User.objects.filter(username=username).first()
            if user is None or not user.is_active:
                messages.error(request, 'Invalid username or password, or account is deactivated.')
                return render(request, 'login/login.html', {'form': form})

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)  # Log the user in
                return redirect('dashboard')  # Redirect to dashboard
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
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


def groups(request):
    groups = Group.objects.all()
    for group in groups:
        print(f"Group: {group.name}, ID: {group.group_id}")  # Debug print
    return render(request, 'groups/groups_list.html', {'groups': groups})


def add_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Group created successfully.")
            return redirect(reverse('groups_list'))
    else:
        form = GroupForm()
    return render(request, 'groups/add_group.html', {'form': form})


def add_user_to_group(request, group_id):
    group = get_object_or_404(Group, group_id=group_id)

    if request.method == "POST":
        user_ids = request.POST.getlist("user_ids")  # Retrieve all selected user IDs
        if user_ids:
            users = User.objects.filter(id__in=user_ids)  # Get User objects for each ID
            group.users.add(*users)  # Add multiple users to the group at once
            group.save()

            # Success message for each added user
            usernames = ', '.join(user.username for user in users)
            messages.success(request, f"{usernames} have been added to the group.")
        else:
            messages.warning(request, "No users were selected.")

        return redirect('group_details', group_id=group.group_id)


def group_details(request, group_id):
    # Use group_id for the lookup
    group = get_object_or_404(Group, group_id=group_id)

    # Get all users not in this group
    available_users = User.objects.exclude(id__in=group.users.values_list('id', flat=True))

    # Update group information if form is submitted
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()  # Strip to remove whitespace
        if not name:
            messages.error(request, "Group name cannot be empty.")
            return redirect('group_details', group_id=group.group_id)

        group.name = name
        group.description = request.POST.get('description', '').strip()

        try:
            group.save()
            messages.success(request, "Group information updated successfully.")
        except IntegrityError as e:
            messages.error(request, f"Failed to update group: {e}")

        return redirect('group_details', group_id=group.group_id)

    context = {
        'group': group,
        'users': available_users,  # Pass only users not in the group
    }
    return render(request, 'groups/group_details.html', context)


def delete_group(request, group_id):
    group = get_object_or_404(Group, group_id=group_id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, "Group deleted successfully.")
        return redirect('groups_list')  # Adjust to the name of your group listing view
    return redirect('group_details', group_id=group.group_id)  # Redirect back if not POST


def remove_user_from_group(request, group_id, user_id):
    group = get_object_or_404(Group, group_id=group_id)
    user = get_object_or_404(User, id=user_id)

    if user in group.users.all():
        group.users.remove(user)
        messages.success(request, f'User {user.username} removed from the group.')
    else:
        messages.error(request, 'User is not in this group.')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'User removed from group.'})
    return redirect('group_details', group_id=group_id)


User = get_user_model()

@login_required
def dashboard(request):
    # Get the total number of active users
    active_users_count = User.objects.filter(is_active=True).count()

    # Check if the user is an employee
    is_employee = hasattr(request.user, 'is_employee') and request.user.is_employee

    # Prepare the context for rendering
    context = {
        'active_users_count': active_users_count,
    }

    # Render to the employee dashboard or the regular dashboard
    if is_employee:
        return render(request, 'courses_details/dashboard_employee.html', context)
    else:
        return render(request, 'courses_details/dashboard.html', context)


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


@user_passes_test(lambda u: u.is_admin)
def manage_users(request):
    # Get the search query from the request
    search_query = request.GET.get('search', '')

    # Filter users based on the search query if it exists
    if search_query:
        users = User.objects.filter(username__icontains=search_query) | User.objects.filter(email__icontains=search_query)
    else:
        users = User.objects.all()

    # Fetch the instructor data associated with each user (if available)
    instructor_data = InstructorData.objects.filter(user__in=users)

    return render(request, 'login/manage_users.html', {'users': users, 'instructor_data': instructor_data, 'search': search_query})


def instructor_detail(request, user_id):
    # Get the user object and associated instructor data
    user = get_object_or_404(User, id=user_id)
    instructor_data = InstructorData.objects.filter(user=user).first()

    # Pass the data to the template
    return render(request, 'login/instructor_detail.html', {'user': user, 'instructor_data': instructor_data})


@user_passes_test(lambda u: u.is_admin)
def change_user_role(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        previous_role = "Admin" if user.is_admin else "Instructor" if user.is_instructor else "Employee"

        new_role = request.POST['role']
        if new_role == 'admin':
            user.is_admin = True
            user.is_instructor = False
            user.is_employee = False
        elif new_role == 'instructor':
            user.is_admin = False
            user.is_instructor = True
            user.is_employee = False
        elif new_role == 'employee':
            user.is_admin = False
            user.is_instructor = False
            user.is_employee = True

        user.save()

        new_role_label = "Admin" if user.is_admin else "Instructor" if user.is_instructor else "Employee"
        messages.success(
            request,
            f"<strong>{user.username}</strong>'s role was successfully updated from <em>{previous_role.capitalize()}</em> to <strong>{new_role_label.capitalize()}</strong>!"
        )
        return redirect('manage_users')


@user_passes_test(lambda u: u.is_admin)
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('manage_users')


@user_passes_test(lambda u: u.is_admin)
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'{user.username} has been deactivated.')
    return redirect('manage_users')

@user_passes_test(lambda u: u.is_admin)
def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'{user.username} has been activated.')
    return redirect('manage_users')


def course_list(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        # Filter courses based on the search query
        courses = Course.objects.filter(course_name__icontains=query)
    else:
        # Retrieve all courses if no query is provided
        courses = Course.objects.all()

    context = {
        'courses': courses,  # List of courses to pass to the template
        'query': query,      # Pass the query to the template for displaying in the search box
    }

    return render(request, 'courses_details/course_list.html', context)  # Adjust the template path as necessary


def add_user_view(request):
    return render(request, 'login/addUser.html')


def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('course_list'))  # Redirect to the course list after saving
    else:
        form = CourseForm()

    return render(request, 'courses_details/add_course.html', {'form': form})


def delete_course(request, course_id):
    # Get the course object or return 404 if not found
    course = get_object_or_404(Course, pk=course_id)

    # Ensure the method is POST to prevent accidental deletions
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('course_list')  # Redirect to the course list page after deletion

    return redirect('course_list')


def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            # Create an Assignment instance
            assignment = Assignment(
                title=form.cleaned_data['title'],
                category=form.cleaned_data['category'],
                description=form.cleaned_data['description'],
                prerequisites=form.cleaned_data['prerequisites'],
                due_date=form.cleaned_data['due_date']
            )
            assignment.save()  # Save the assignment to the database

            # Redirect to the add_questions page with the assignment title
            return redirect('add_questions', assignment_title=assignment.title)  # Pass the title here
    else:
        form = AssignmentForm()

    return render(request, 'assignments/create_assignment.html', {'form': form})


def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments})


def add_questions(request, assignment_title):
    # Pass the assignment_title to the template
    context = {
        'assignment_title': assignment_title,
        'questions': Question.objects.filter(assignment__title=assignment_title),  # Fetch questions related to this assignment
    }
    return render(request, 'assignments/add_questions.html', context)


def submit_questions(request, assignment_title):
    # Fetch the assignment object using the title
    assignment = Assignment.objects.filter(title=assignment_title).first()
    if not assignment:
        raise Http404("Assignment not found.")

    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        subtitle = request.POST.get('subtitle')
        question_type = request.POST.get('question_type')
        answer_type = request.POST.get('answer_type')
        file_upload = request.FILES.get('file_upload')

        # Save the question to the database
        question = Question.objects.create(
            text=question_text,
            subtitle=subtitle,
            question_type=question_type,
            answer_type=answer_type,
            file_upload=file_upload,
            assignment=assignment  # Associate the question with the assignment
        )

        return redirect('add_questions', assignment_title=assignment_title)  # Redirect back to the add_questions page

    # To display previously uploaded files if applicable
    questions = Question.objects.filter(assignment=assignment)

    return render(request, 'assignments/add_questions.html', {
        'assignment_title': assignment_title,
        'questions': questions,  # Pass uploaded questions to the template
    })


def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.file_upload.delete(save=False)  # Delete the file from the filesystem
        question.delete()  # Delete the question from the database
        return redirect('add_questions', assignment_title=question.assignment.title)  # Redirect to add_questions with the assignment title

    return redirect('add_questions', assignment_title=question.assignment.title)  # Redirect if the request is not POST


def fetch_questions(request, assignment_title):
    questions = Question.objects.filter(assignment__title=assignment_title)  # Adjust the query as needed
    return render(request, 'assignments/fetch_questions.html', {
        'assignment_title': assignment_title,
        'questions': questions,
    })


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    contents = course.contents.all()

    # Fetch the progress of each content for the current user
    user_progress = {progress.content.id: progress.completed for progress in UserProgress.objects.filter(user=request.user, content__course=course)}
    completed_count = sum(1 for progress in user_progress.values() if progress)
    total_count = contents.count()
    progress_percentage = (completed_count / total_count) * 100 if total_count > 0 else 0

    context = {
        'course': course,
        'contents': contents,
        'user_progress': user_progress,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'progress_track/course_detail.html', context)


@login_required
def update_progress(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    progress, created = UserProgress.objects.get_or_create(user=request.user, content=content)
    progress.completed = not progress.completed  # Toggle the completed status
    progress.save()

    return redirect('progress_track/course_detail', course_id=content.course.id)


def course_progress(request):
    # Example of fetching a course and progress for a user (this assumes you're logged in)
    user = request.user
    course = Course.objects.first()  # Get the first course, adjust based on logic
    user_progress = UserProgress.objects.filter(user=user)

    progress_percentage = 45  # For example, hardcoded progress (replace with dynamic logic)

    context = {
        'course': course,
        'progress_percentage': progress_percentage,
        'user_progress': user_progress,
    }

    return render(request, 'progress_track/course_detail.html', context)


def vimeo_video_view(request):
    video_id = "1020066578"  # Replace with your video ID or pass it dynamically
    context = {
        'video_id': video_id,
    }
    return render(request, 'progress_track/vimeo_video.html', context)


def portal_info(request):
    return render(request, 'courses_details/portal_info.html')
