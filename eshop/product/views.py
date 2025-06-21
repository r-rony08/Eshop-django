from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
# Create your views here.

@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()

    serializer = ProductSerializer(products, many=True)
    return Response({"products": serializer.data})