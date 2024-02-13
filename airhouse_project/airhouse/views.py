from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView 
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterForm
from .models import InventoryItem, Category

class Index(TemplateView):
    template_name = 'airhouse/index.html'

class LoginView(LoginView):
    template_name = 'airhouse/login.html'

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')

        return render(request, 'airhouse/dashboard.html', {'items': items})

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
    form_class = InventoryItem
    template_name = 'airhouse/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.username
        return super().form_valid(form)