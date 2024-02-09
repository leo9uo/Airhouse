from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View 
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm

class Index(TemplateView):
    template_name = 'airhouse/index.html'

def login_view(request):
    return render(request, 'airhouse/login.html')

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