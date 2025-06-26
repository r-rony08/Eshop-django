from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *
from .filters import *
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    filterset = OrderFilter(request.GET, queryset=Order.objects.all().order_by('id'))
    count = filterset.qs.count()
    # paginations
    perpage = 3
    paginator = PageNumberPagination()
    paginator.page_size = perpage
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = OrderSerializer(queryset, many=True)
    return Response({
        "count": count,
        "perpage": perpage,
        "orders": serializer.data
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_order(request, pk):
    orders = get_object_or_404(Order, id=pk)
    serializers = OrderSerializer(orders, many=False)
    return Response({'order': serializers.data})


@api_view(['POST'])
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
            product = product.objects.get(id=i['product'])
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


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
#@permission_classes([IsAuthenticated, IsAdminUser])
def process_order(request, pk):
    order = get_object_or_404(Order, id=pk)

    order.status = request.data['status']
    order.save()

    order.payment_status = request.data['payment_status']
    order.save()

    serializers = OrderSerializer(order, many=False)
    return Response({'order': serializers.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    orders = get_object_or_404(Order, id=pk)

    orders.delete()
    
    serializers = OrderSerializer(orders, many=False)
    return Response({'Details': 'Order is deleted'})

