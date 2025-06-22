from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):

    keyword = filters.CharFilter(field_name="name", lookup_expr="icontains")
    initial_buying_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    initial_selling_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ('keyword', 'Categories', 'brand', 'initial_buying_price', 'initial_selling_price')