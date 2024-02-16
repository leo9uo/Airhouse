from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterForm, InventoryItemForm
from .models import InventoryItem, Category, Order
from airhouse_project.settings import LOW_QUANTITY
from django.contrib import messages

class Index(TemplateView):
    template_name = 'airhouse/index.html'

class LoginView(LoginView):
    template_name = 'airhouse/login.html'

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')

        low_inventory = InventoryItem.objects.filter(
            user=self.request.user.id,
            quantity__lte=LOW_QUANTITY
        )

        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'{low_inventory.count()} items have low inventory')
            else:
                messages.error(request, f'{low_inventory.count()} item has low inventory')

        low_inventory_ids = InventoryItem.objects.filter(
            user=self.request.user.id,
            quantity__lte=LOW_QUANTITY
        ).values_list('id', flat=True)

        return render(request, 'airhouse/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})
    

class Orders(ListView):
    model = Order
    template_name = 'airhouse/orders.html'
    context_object_name = 'orders'

class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'airhouse/signup.html', {'form': form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # This saves the user instance
            
            
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            
            # Authenticate the user
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                # If authentication fails, handle it (e.g., return an error message)
                form.add_error(None, "Authentication failed.")
        # If form is not valid or authentication fails, re-render the form with errors
        return render(request, 'airhouse/signup.html', {'form': form})
    
class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'airhouse/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'airhouse/item_form.html'
    success_url = reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'airhouse/delete_item.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'