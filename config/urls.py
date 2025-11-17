"""
URL configuration for credentials project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Credentials Portal</h1><p>Access requires a valid token link.</p><p><a href="/admin/">Admin Login</a></p>')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('credentials/', include('credentials.urls')),
    path('', home, name='home'),
]
