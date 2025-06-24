from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
# Create your views here.

@api_view(['GET'])
def get_products(request):
    filterset = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    count = filterset.qs.count()
    # Pagination
    perpage = 3
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
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        product = Product.objects.create(**data, user=request.user)
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
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    # Check if user is same-todo
    if product.user != request.user:
        return Response({'error': 'You cannot Update this product'}, status=status.HTTP_403_FORBIDDEN)

    product.name = request.data['name']
    product.description = request.data['description']
    product.brand = request.data['brand']
    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response({"product": serializer.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    # Check if user is same-todo
    if product.user != request.user:
        return Response({'error': 'You cannot delete this product'}, status=status.HTTP_403_FORBIDDEN)
    args = {'product':pk}
    images = ProductImage.objects.filter(**args)
    for i in images:
        i.delete()
        
    product.delete
    return Response({'details':'product is deleted'}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    user = request.user
    product = get_object_or_404(product, id=pk)
    data = request.data

    review = product.reviews.filter(user=user)

    if data['rating'] <= 0 or data['rating'] > 5:
        return Response({'error':'Please select rating between 1-5'}, status=status.HTTP_400_BAD_REQUEST)
    
    elif review.exists():
        new_review = { 'rating': data['rating'], 'comment': data['comment']}
        review.update(**new_review)
        rating = product.reviews.aggregate(avg_rating=Avg('rating'))
        product.rating = rating['avg_rating']
        product.save()
        return Response({'detail': 'Review Updated'})
    
    else:
        Review.objects.create(
            user = user,
            product = product,
            rating = data['rating'],
            comment = data['comment'],
        )
        rating = product.reviews.aggregate(avg_rating=Avg('rating'))
        product.rating = rating['avg_rating']
        product.save()
        return Response({'detail': 'Review Posted'})
    


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    user = request.user
    product = get_object_or_404(product, id=pk)
    review = product.reviews.filter(user=user)

    if review.exists():
        review.delete()

        rating = product.reviews.aggregate(avg_rating=Avg('rating'))
        if rating['avg_rating'] is None:
            rating['avg_rating'] = 0

        product.rating = rating['avg_rating']
        product.save()
        return Response({'detail': 'Review Deleted'})

    else:
        return Response({'error':'Review Not Found'}, status=status.HTTP_404_NOT_FOUND)