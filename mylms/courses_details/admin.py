from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, InstructorData


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_employee', 'is_instructor')}),
    )


class InstructorDataAdmin(admin.ModelAdmin):
    list_display = ('instructorName', 'instructorQualification', 'user')


admin.site.register(User, UserAdmin)
admin.site.register(InstructorData, InstructorDataAdmin)
