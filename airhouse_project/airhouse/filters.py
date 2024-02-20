from django_filters import FilterSet, CharFilter, DateFilter
from django.forms.widgets import TextInput, DateInput
from .models import *

class OrderFilter(FilterSet):
    order_date = DateFilter(widget=DateInput(attrs={'placeholder': 'Order Date', 'class': 'form-control'}))
    recipient = CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Recipient', 'class': 'form-control'}))
    order_source = CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Order Source', 'class': 'form-control'}))
    skus_ordered = CharFilter(field_name='skus_ordered__name', lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'SKUs Ordered', 'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['order_date', 'status', 'payment', 'order_source', 'recipient', 'skus_ordered']

