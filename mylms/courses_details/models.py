
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
from django.db import models


class User(AbstractUser):
    # user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    is_instructor = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description provided")  # Set a default value here
    users = models.ManyToManyField(User, related_name='group_users')


class InstructorData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_data', null=True, blank=True)
    instructor_id = models.AutoField(primary_key=True)
    instructorName = models.CharField(max_length=100)
    instructorQualification = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.instructorName} - {self.instructorQualification}"


# class Role(models.Model):
#     role_id = models.AutoField(primary_key=True)
#     role_name = models.CharField(max_length=150, unique=True)
#     role_code = models.CharField(max_length=50, unique=True)
#     role_type = models.CharField(max_length=50)
#     role_status = models.BooleanField(default=True)
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     created_by = models.CharField(max_length=150)
#     creation_date = models.DateTimeField(auto_now_add=True)
#     last_update_date = models.DateTimeField(auto_now=True)
#     last_update_login = models.CharField(max_length=150, null=True, blank=True)
#     last_updated_by = models.CharField(max_length=150)
#
#     def __str__(self):
#         return self.role_name


# class RoleAssignment(models.Model):
#     role_assignment_id = models.AutoField(primary_key=True)
#     role_id = models.ForeignKey('Role', on_delete=models.CASCADE)
#     id = models.ForeignKey('User', on_delete=models.CASCADE)
#     role_type = models.CharField(max_length=50)
#     delete_flag = models.BooleanField(default=False)
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     created_by = models.CharField(max_length=150)
#     creation_date = models.DateTimeField(auto_now_add=True)
#     last_update_date = models.DateTimeField(auto_now=True)
#     last_update_login = models.CharField(max_length=150, null=True, blank=True)
#     last_updated_by = models.CharField(max_length=150)
#
#     def __str__(self):
#         return f"Role Assignment: {self.role_id} to {self.user_id}"


class CourseModule(models.Model):
    course_module_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=150)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_by = models.CharField(max_length=150)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_update_login = models.CharField(max_length=150, null=True, blank=True)
    last_updated_by = models.CharField(max_length=150)

    def __str__(self):
        return self.module_name


class CourseTracking(models.Model):
    tracking_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    module_id = models.ForeignKey('CourseModule', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    id = models.ForeignKey('User', on_delete=models.CASCADE)
    progress_status = models.CharField(max_length=50)
    active_flag = models.BooleanField(default=True)
    percent_tracking = models.DecimalField(max_digits=5, decimal_places=2)  # Example: 99.99%
    module_status = models.CharField(max_length=50)
    module_start_time = models.DateTimeField(null=True, blank=True)
    module_end_time = models.DateTimeField(null=True, blank=True)
    overall_status = models.CharField(max_length=50)
    created_by = models.CharField(max_length=150)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_update_login = models.CharField(max_length=150, null=True, blank=True)
    last_updated_by = models.CharField(max_length=150)

    def __str__(self):
        return f"Tracking ID: {self.tracking_id} | User: {self.user_id} | Module: {self.module_id}"


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=50, unique=True)
    course_name = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    course_content = models.TextField()
    course_type = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    course_url = models.URLField(max_length=255, null=True, blank=True)
    created_by = models.CharField(max_length=150)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    last_update_login = models.CharField(max_length=150, null=True, blank=True)
    last_updated_by = models.CharField(max_length=150)

    def __str__(self):
        return self.course_name


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=[('Programming', 'Programming'), ('Science', 'Science')])
    description = models.TextField(blank=True)  # Make description optional
    prerequisites = models.CharField(max_length=255, blank=True)  # Make prerequisites optional
    due_date = models.DateField(null=True, blank=True)  # Make due_date optional


class Question(models.Model):
    text = models.TextField()
    subtitle = models.TextField(blank=True, null=True)
    question_type = models.CharField(max_length=50)
    answer_type = models.CharField(max_length=50)
    file_upload = models.FileField(upload_to='uploads/', blank=True, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)  # Assuming a relationship to Assignment


class Content(models.Model):
    COURSE_CONTENT_TYPES = [
        ('video', 'Video'),
        ('article', 'Article'),
        ('paragraph', 'Paragraph'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=10, choices=COURSE_CONTENT_TYPES)
    content_url = models.URLField(null=True, blank=True)  # For video or article
    text_content = models.TextField(null=True, blank=True)  # For paragraphs

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.content.title} - {"Completed" if self.completed else "Incomplete"}'
