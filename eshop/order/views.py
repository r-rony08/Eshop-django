from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *
#from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data
    order_items = data['orderitems']

    if order_items and len(order_items) == 0:
        return Response({'error': 'No order item. Please Add aileast one item'}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        # Create Order

        total_amount =sum(item['price'] * item['quantity'] for item in order_items)

        order = Order.objects.create(
            user = user,
            street = data['street'],
            city = data['city'],
            country = data['country'],
            zip_code = data['zip_code'],
            state = data['state'],
            Phon_num = data['Phon_num'],

            total_amount = total_amount
        )

        # Create Order Item and set order to order item
        for i in order_items:
            product = product.objects.get(id=1['product'])
            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                quantity = i['quantity'],
                price = i['price']
            )

            # Update Product Stock
            product.stock -=item.quantity
            product.save()
            serializers = OrderSerializer(order, many=True)
            return Response(serializers.data)



