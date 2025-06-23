from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product,ProductImage
from .serializers import ProductSerializer, ProductImagesSerializer
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
# Create your views here.

@api_view(['GET'])
def get_products(request):
    filterset = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    count = filterset.qs.count()
    # Pagination
    perpage = 1
    paginator = PageNumberPagination()
    paginator.page_size = perpage
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ProductSerializer(queryset, many=True)
    return Response({
        "count": count,
        "perpage": perpage,
        "products": serializer.data
        })

@api_view(['GET'])
def get_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response({"product": serializer.data})

@api_view(['GET'])
def new_product(request):
    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        product = Product.objects.create(**data)
        res = ProductSerializer(product, many=False)
        return Response({"product": res.data})
    else:
        return Response(serializer.errors)

@api_view(['POST'])
def upload_product_images(request):
    data = request.data
    files = request.FILES.getlist('images')
    images = []
    for f in files:
        image = ProductImage.objects.create(product=Product(data['product']), image=f)
        images.append(image)
    serializer = ProductImagesSerializer(images, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    # Check if user is same-todo
    product.name = request.data['name']
    product.description = request.data['description']
    product.brand = request.data['brand']
    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response({"product": serializer.data})

@api_view(['DELETE'])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    # Check if user is same-todo

    args = {'product':pk}
    images = ProductImage.objects.filter(**args)
    for i in images:
        i.delete()
        
    product.delete
    return Response({'details':'product is deleted'}, status=status.HTTP_200_OK)