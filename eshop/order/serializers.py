from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields ="__all__"

class OrderSerializer(serializers.ModelSerializer):

    OrderItem = serializers.SerializerMethodField(method_name='get_order_items', read_only=True)

    class Meta:
        model = Order
        fields ="__all__"

    def get_order_items(self, obj):
        order_items = obj.orderitems.all()
        serializers = OrderItemSerializer(order_items, many=True)
        return serializers.data


