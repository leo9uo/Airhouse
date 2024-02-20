from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterForm, InventoryItemForm, OrderForm, OrderItemFormSet
from django_filters.views import FilterView
from .filters import OrderFilter
from .models import InventoryItem, Category, Order
from airhouse_project.settings import LOW_QUANTITY
from django.contrib import messages

class Index(TemplateView):
    template_name = 'airhouse/index.html'

class LoginView(LoginView):
    template_name = 'airhouse/login.html'

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
    

class Dashboard(View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=request.user.id).order_by('id')
        low_inventory = items.filter(quantity__lte=LOW_QUANTITY)

        # # Fetch the names of items with low inventory
        # low_inventory_items = low_inventory.values_list('name', flat=True)

        # # Generate a comma-separated string of item names
        # low_inventory_item_names = ', '.join(low_inventory_items)

        if low_inventory.count() > 0:
            message_text = f'{low_inventory.count()} item{"s" if low_inventory.count() > 1 else ""} {"have" if low_inventory.count() > 1 else "has"} low inventory.'
            messages.error(request, message_text)

        low_inventory_ids = low_inventory.values_list('id', flat=True)

        return render(request, 'airhouse/dashboard.html', {
            'items': items,
            'low_inventory_ids': low_inventory_ids
        })


# INVENTORY ITEMS
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

# ORDERS
class Orders(FilterView):
    model = Order
    template_name = 'airhouse/orders.html'
    context_object_name = 'orders'
    filterset_class = OrderFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myFilter'] = OrderFilter(self.request.GET, queryset=self.get_queryset())
        return context


class OrderDetail(DetailView):
    model = Order
    template_name = 'airhouse/order_detail.html'
    context_object_name = 'order'


class AddOrder(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'airhouse/order_form.html'
    success_url = reverse_lazy('orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['formset']
        if orderitems.is_valid():
            self.object = form.save()
            orderitems.instance = self.object
            orderitems.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EditOrder(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'airhouse/order_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(EditOrder, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            response = super(EditOrder, self).form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('order-detail', kwargs={'pk': self.object.pk})

class DeleteOrder(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'airhouse/delete_order.html'
    success_url = reverse_lazy('orders')
    context_object_name = 'order'


class Restock(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=request.user.id).order_by('id')
        low_inventory = items.filter(quantity__lte=LOW_QUANTITY)
        low_inventory_ids = low_inventory.values_list('id', flat=True)

        return render(request, 'airhouse/restock.html', {
            'items': items,
            'low_inventory_ids': low_inventory_ids
        })