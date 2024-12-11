from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses_details.urls')),

    path('accounts/', include('allauth.urls')),     # For Google OAuth

    # path('auth/', include('social_django.urls', namespace='social')),  # Make sure this line is included

]
