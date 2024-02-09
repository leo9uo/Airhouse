from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('register/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='airhouse/login'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='/logout'), name='logout')
]