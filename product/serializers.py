from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = models.Product
        # fields = '__all__'
        fields = [
            'id', 'code', 'name', 'image', 'description', 
            'product_quantity', 'unit', 'purchase_price', 
            'sales_price', 'stock_quantity', 'date', 'user', 'category'
        ]
        extra_kwargs = {'user': {'read_only': True}} 

    def get_image(self, obj):
        if obj.image:
            return obj.image.url  # Returns the full Cloudinary URL
        return obj

