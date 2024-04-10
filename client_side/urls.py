from django.urls import path
from .views import Index, SignUpView, LoginView, AvailableInventoryListView, AddToCart, CartList, EditCartItem, RemoveCartItem, Orders, CheckoutView, OrderConfirmationView
from django.contrib.auth import views as auth_views

app_name = 'customer'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='client/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='client/logout.html'), name='logout'),
    path('inventory/', AvailableInventoryListView.as_view(), name='inventory'),
    path('cart/', CartList.as_view(), name='cart'),
    path('add-to-cart/<int:inventory_item_id>/', AddToCart.as_view(), name='add-to-cart'),
    path('edit-cart-item/<int:item_id>/', EditCartItem.as_view(), name='edit-cart-item'),
    path('remove-from-cart/<int:item_id>/', RemoveCartItem.as_view(), name='remove-from-cart'),
    path('orders/', Orders.as_view(), name='orders'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-confirmation/<int:order_id>/', OrderConfirmationView.as_view(), name='order-confirmation'),
]
