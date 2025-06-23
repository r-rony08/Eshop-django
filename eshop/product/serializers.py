from rest_framework import serializers
from .models import Product, ProductImage

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    images = ProductImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('name', 'description', 'brand', 'images', 'Categories')
        #fields = ('name', 'initial_selling_price')
        extra_kwargs = {
            "name": {"required":True, 'allow_blank':False},
            "description": {"required":True, 'allow_blank':False},
            "brand": {"required":True, 'allow_blank':False},
            "Categories": {"required":True, 'allow_blank':False},
        }

       