from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)


class InstructorData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_data', null=True, blank=True)
    instructorName = models.CharField(max_length=100)
    instructorQualification = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.instructorName} - {self.instructorQualification}"