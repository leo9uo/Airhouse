from django import forms
from .models import CustomUser, CustomerProfile

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [ 'first_name', 'last_name', 'email', 'password',]

class CustomerProfileForm(forms.ModelForm):
    expiration_date = forms.DateField(
    label='Expiration Date (MM/YY)',
    input_formats=['%m/%y'],
    widget=forms.DateInput(format='%m/%y'),
    )
    class Meta:
        model = CustomerProfile
        fields = ['address', 'city', 'state', 'credit_card_number', 'expiration_date', 'cvv']
