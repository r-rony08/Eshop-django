from rest_framework import serializers
from .models import *


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"




class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    images = ProductImagesSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField(method_name='get_reviews')

    class Meta:
        model = Product
        fields = ('name', 'description', 'brand', 'Categories', 'user', 'price', 'images', 'rating', 'reviews')
        #fields = ('name', 'initial_selling_price')
        extra_kwargs = {
            "name": {"required":True, 'allow_blank':False},
            "description": {"required":True, 'allow_blank':False},
            "brand": {"required":True, 'allow_blank':False},
            "Categories": {"required":True, 'allow_blank':False},
        }

    def get_reviews(self, obj):
        Reviews = obj.reviews.all()
        serializers = ReviewSerializer(Reviews, many=True)
        return serializers.data