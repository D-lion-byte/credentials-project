from django.urls import path
from . import views

app_name = 'credentials'

urlpatterns = [
    path('info/<str:token>/', views.info_page, name='info_page'),
    path('update/<str:token>/', views.update_credentials_via_token, name='update_via_token'),
    path('success/', views.update_success, name='update_success'),
]
