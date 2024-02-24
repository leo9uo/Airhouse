from django import forms
from django_filters import FilterSet, CharFilter, ChoiceFilter, DateFilter
from django.forms.widgets import TextInput, DateInput
from .models import *

class OrderFilter(FilterSet):
    order_date = DateFilter(widget=DateInput(attrs={'type': 'date', 'placeholder': 'Order Date', 'class': 'form-control'}))
    recipient = CharFilter(lookup_expr='istartswith', widget=TextInput(attrs={'placeholder': 'Recipient', 'class': 'form-control'}))
    order_source = CharFilter(lookup_expr='istartswith', widget=TextInput(attrs={'placeholder': 'Order Source', 'class': 'form-control'}))
    skus_ordered = CharFilter(method='filter_skus_ordered', widget=TextInput(attrs={'placeholder': 'SKUs Ordered', 'class': 'form-control'}))

    status = ChoiceFilter(choices=[('', 'Order Status ⧨'),] + Order.STATUS_CHOICES, empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    payment = ChoiceFilter(choices=[('', 'Payment Status ⧨'),] + Order.PAYMENT_STATUS_CHOICES, empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['order_date', 'status', 'payment', 'order_source', 'recipient']

    def filter_skus_ordered(self, queryset, name, value):
        return queryset.filter(order_items__inventory_item__name__icontains=value).distinct()

class InventoryFilter(FilterSet):
    name = CharFilter(lookup_expr='istartswith', widget=TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    quantity = CharFilter(lookup_expr='istartswith', widget=TextInput(attrs={'placeholder': 'Quantity', 'class': 'form-control'}))
    price = CharFilter(lookup_expr='istartswith', widget=TextInput(attrs={'placeholder': 'Price', 'class': 'form-control'}))
    category = CharFilter(field_name='category__name', lookup_expr='istartswith', widget=TextInput(attrs={'placeholder': 'Category', 'class': 'form-control'}))

    