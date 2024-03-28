from django import forms
from django_filters import FilterSet, CharFilter
from django.forms.widgets import TextInput
from airhouse.models import InventoryItem

class InventoryFilter(FilterSet):
    company_name = CharFilter(field_name='user__company_name', lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Company Name', 'class': 'form-control'}))
    name = CharFilter(lookup_expr='istartswith', widget=TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    quantity = CharFilter(lookup_expr='istartswith', widget=TextInput(attrs={'placeholder': 'Quantity', 'class': 'form-control'}))
    price = CharFilter(lookup_expr='istartswith', widget=TextInput(attrs={'placeholder': 'Price', 'class': 'form-control'}))

    class Meta:
        model = InventoryItem
        fields = ['company_name', 'name', 'quantity', 'price']