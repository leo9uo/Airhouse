from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import SignUpForm, CustomerProfileForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from airhouse.models import InventoryItem


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


class AvailableInventoryListView(ListView):
    template_name = 'client/avail_inv_list.html'
    model = InventoryItem
    context_object_name = 'inventory_items'

    def get_queryset(self):
        return InventoryItem.objects.all()