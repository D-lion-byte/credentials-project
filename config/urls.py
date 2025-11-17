"""
URL configuration for credentials project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('credentials/', include('credentials.urls')),
    path('', lambda request: redirect('credentials:info_page', token=''), name='home'),
]
