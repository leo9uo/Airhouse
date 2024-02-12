from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, MyLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='/logout'), name='logout')
]