import django_filters

from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['order_date', 'status', 'payment', 'order_source', 'recipient', 'skus_ordered']