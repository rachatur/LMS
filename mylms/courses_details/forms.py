from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Course
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )


class SignUpForm(UserCreationForm):
    # email = forms.EmailField(
    #     widget=forms.EmailInput()
    # )

    # The Meta class specifies the model to be used
    class Meta:
        # link the form with the custom user model, this form will create & modify instance of the model
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
        # fields = ['name', 'description', 'branch', 'price', 'users']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'start_date', 'end_date', 'course_content', 'course_type', 'description', 'course_url', 'created_by', 'last_update_login', 'last_updated_by']



class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'category', 'description', 'prerequisites', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prerequisites': forms.TextInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class QuestionForm(forms.Form):
    question_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    subtitle = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    question_type = forms.ChoiceField(
        choices=[('MCQ', 'Multiple Choice'), ('Text Input', 'Text Input'), ('File Upload', 'File Upload')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    answer_type = forms.ChoiceField(
        choices=[('Single', 'Single Choice'), ('Multiple', 'Multiple Choice')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    file_upload = forms.FileField(required=False)   # File upload field