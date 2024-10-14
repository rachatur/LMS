from courses_details import views
from django.urls import path
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('my_courses/', views.my_courses, name='my_courses'),
    path('about_us/',views.about_us, name='about_us'),
    path('contact_us/',views.contact_us, name='contact_us'),
    path('instructor/',views.instructor, name='instructor'),
    path('my_courses/',views.my_courses, name='my_courses'),
    # path('login/',views.login, name='login'),
    path('profile/',views.profile, name='profile'),
    # path('register/',views.register, name='register'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # path('home/', views.home, name='home'),  # Define your home view accordingly

    path('admin/',views.admin, name='admin'),

    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('reset-password/', views.reset_password_view, name='password_reset'),
]
