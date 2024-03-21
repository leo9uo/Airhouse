from django.urls import path
from .views import Index, SignUpView

app_name = 'customer'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
]