from django.urls import path
from .views import Index, SignUpView, LoginView, AvailableInventoryListView, AddToCart
from django.contrib.auth import views as auth_views

app_name = 'customer'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='client/login.html'), name='login'),
    path('inventory/', AvailableInventoryListView.as_view(), name='inventory'),
    path('add-to-cart/<int:inventory_item_id>/', AddToCart.as_view(), name='add-to-cart'),
]