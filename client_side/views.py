from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .forms import SignUpForm, CustomerProfileForm
from .filters import InventoryFilter
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from airhouse.models import InventoryItem, Order, OrderItem
from .models import Cart, CartItem


class Index(TemplateView):
    template_name = 'client/index.html'


class LoginView(LoginView):
    template_name = 'client/login.html'
    
    def get_success_url(self):
        return reverse('customer:index')


class SignUpView(View):
    def get(self, request):
        user_form = SignUpForm()
        profile_form = CustomerProfileForm()
        return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})
    
    def post(self, request):
        user_form = SignUpForm(request.POST)
        profile_form = CustomerProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('customer:index')  
        return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})


class AvailableInventoryListView(LoginRequiredMixin, TemplateView):
    template_name = 'client/avail_inv_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventory_items = InventoryItem.objects.all()
        inventory_filter = InventoryFilter(self.request.GET, queryset=inventory_items)
        filtered_items = inventory_filter.qs

        context['inventory_items'] = filtered_items
        context['filter'] = inventory_filter

        return context
    

class AddToCart(View):
    def post(self, request, *args, **kwargs):
        # Get the inventory item
        inventory_item_id = kwargs.get('inventory_item_id')
        inventory_item = InventoryItem.objects.get(id=inventory_item_id)
        
        # Get or create the cart for the current user
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Retrieve quantity from the form data
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided
        
        # Check if the item is already in the cart
        existing_cart_item = CartItem.objects.filter(cart=cart, inventory_item=inventory_item).first()
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            CartItem.objects.create(cart=cart, inventory_item=inventory_item, quantity=quantity)
        
        return redirect('customer:inventory')

    

class CartList(LoginRequiredMixin, TemplateView):
    template_name = 'client/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the user's cart items
        user_cart = Cart.objects.get_or_create(user=self.request.user)[0]
        cart_items = user_cart.cart_items.all()

        context['cart_items'] = cart_items

        return context


class EditCartItem(LoginRequiredMixin, View):
    def post(self, request, item_id):
        quantity = request.POST.get('quantity')
        cart_item = get_object_or_404(CartItem, pk=item_id)
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('customer:cart')
    

    
class RemoveCartItem(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, pk=item_id)
        cart_item.delete()
        return redirect('customer:cart')
    
class Orders(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
        # Get orders placed by the logged-in user
        orders = Order.objects.filter(user=request.user)

        # Render the template with the orders queryset
        return render(request, 'orders.html', {'orders': orders})
     
class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        # Get the user's cart
        cart = Cart.objects.get(user=request.user)
        
        # Create an order for the user (using the Order model from the airhouse app)
        order = Order.objects.create(recipient=request.user.email, order_source='Airhouse')
        
        # Create order items for each item in the cart
        for cart_item in cart.cart_items.all():
            order_item = OrderItem.objects.create(order=order, inventory_item=cart_item.inventory_item, quantity=cart_item.quantity)
            # Update the inventory quantity (decrease)
            inventory_item = cart_item.inventory_item
            inventory_item.quantity -= cart_item.quantity
            inventory_item.save()
        
        # Clear the user's cart
        cart.cart_items.all().delete()
        
        return redirect('customer:order-confirmation', order_id=order.id)  # Redirect to the order confirmation page
    

class OrderConfirmationView(View):
        def get(self, request, *args, **kwargs):
            # Get the order object from the database
            order_id = kwargs.get('order_id')
            order = Order.objects.get(id=order_id)
            
            # Render the order confirmation template with the order object
            return render(request, 'order_confirmation.html', {'order': order})