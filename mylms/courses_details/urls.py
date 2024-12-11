from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my_courses/', views.my_courses, name='my_courses'),
    path('about_us/',views.about_us, name='about_us'),
    path('contact_us/',views.contact_us, name='contact_us'),
    path('instructor/',views.instructor, name='instructor'),
    path('my_courses/',views.my_courses, name='my_courses'),
    path('course_store/', views.course_store, name='course_store'),
    path('profile/',views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/', views.admin, name='admin'),
    path('portal/', views.portal_info, name='portal'),

    path('groups/', views.groups, name='groups_list'),
    path('groups/add/', views.add_group, name='add_group'),
    path('groups/<int:group_id>/add_user/', views.add_user_to_group, name='add_user_to_group'),
    path('groups/<int:group_id>/', views.group_details, name='group_details'),
    path('group/<int:group_id>/remove_user/<int:user_id>/', views.remove_user_from_group, name='remove_user_from_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('reset-password/', views.reset_password_view, name='password_reset'),

    path('manage_users/', views.manage_users, name='manage_users'),
    path('instructor/<int:user_id>/', views.instructor_detail, name='instructor_detail'),
    path('change_user_role/<int:user_id>/', views.change_user_role, name='change_user_role'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('addUser/', views.add_user_view, name='addUser'),

    path('course_list/', views.course_list, name='course_list'),
    path('add/', views.add_course, name='add_course'),  # Ensure this line is added
    path('course/delete/<int:course_id>/', views.delete_course, name='delete_course'),

    path('assignments/', views.assignment_list, name='assignment_list'),
    path('create_assignment/', views.create_assignment, name='create_assignment'),
    path('add_questions/<str:assignment_title>/', views.add_questions, name='add_questions'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('submit_questions/<str:assignment_title>/', views.submit_questions, name='submit_questions'),  # Ensure this is defined
    path('fetch_questions/<str:assignment_title>/', views.fetch_questions, name='fetch_questions'),  # Add this line

    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('update_progress/<int:content_id>/', views.update_progress, name='update_progress'),
    path('pgtrack/', views.course_progress, name='pgtrack'),  # Course progress URL
    path('vimeo/', views.vimeo_video_view, name='vimeo_video'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
