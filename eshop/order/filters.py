from django_filters import rest_framework as filters
from .models import *

class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = ('id', 'status', 'payment_status', 'payment_mode')