from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, InventoryItem, Category, Order, OrderItem

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    company_name = forms.CharField(max_length=100, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address.')
    invitation_code = forms.CharField(max_length=100, required=True, help_text='Required.')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'company_name', 'email', 'password1', 'password2', 'invitation_code')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Enter a password.'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'
        # Optionally, reorder fields if needed
        self.order_fields(('first_name', 'last_name', 'company_name', 'email', 'password1', 'password2', 'invitation_code'))


class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'price', 'category']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['recipient', 'status', 'payment', 'order_source']

#inline formset for OrderItems
OrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    fields=('inventory_item', 'quantity',),
    extra=1, 
    can_delete=False
)

