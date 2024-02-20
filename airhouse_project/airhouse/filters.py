import django_filters
from django import forms

from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class OrderFilter(django_filters.FilterSet):
    # use for date field UI on orders filter
    order_date = django_filters.DateFilter(field_name='order_date', widget=DateInput())
    
    class Meta:
        model = Order
        fields = ['order_date', 'status', 'payment', 'order_source', 'recipient', 'skus_ordered']




