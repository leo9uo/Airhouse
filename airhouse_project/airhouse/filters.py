from django_filters import FilterSet, CharFilter, DateFilter
from django.forms.widgets import TextInput, DateInput
from .models import *

class OrderFilter(FilterSet):
    order_date = DateFilter(widget=DateInput(attrs={'type': 'date', 'placeholder': 'Order Date', 'class': 'form-control'}))
    recipient = CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Recipient', 'class': 'form-control'}))
    order_source = CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Order Source', 'class': 'form-control'}))
    skus_ordered = CharFilter(method='filter_skus_ordered', widget=TextInput(attrs={'placeholder': 'SKUs Ordered', 'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['order_date', 'status', 'payment', 'order_source', 'recipient']

    def filter_skus_ordered(self, queryset, name, value):
        return queryset.filter(order_items__inventory_item__name__icontains=value).distinct()
