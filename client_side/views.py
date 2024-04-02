from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import SignUpForm, CustomerProfileForm
from .filters import InventoryFilter
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from airhouse.models import InventoryItem
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
        
        # Check if the item is already in the cart
        existing_cart_item = CartItem.objects.filter(cart=cart, inventory_item=inventory_item).first()
        if existing_cart_item:
            existing_cart_item.quantity += 1
            existing_cart_item.save()
        else:
            CartItem.objects.create(cart=cart, inventory_item=inventory_item, quantity=1)
        
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
