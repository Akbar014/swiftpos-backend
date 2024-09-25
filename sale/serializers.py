from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from product import models as product_models


class SaleItemsSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=product_models.Product.objects.all())

    class Meta:
        model = models.SaleItems
        fields = ['product', 'quantity', 'unit_price']

    


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemsSerializer(many=True)
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.Sale
        fields = ['id', 'code', 'user', 'customer', 'total_amount', 'discount', 'sale_date', 'items' ]

    

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        sale = models.Sale.objects.create(**validated_data)
        # print("Created Sale:", sale)

        for item_data in items_data:
            models.SaleItems.objects.create(sale=sale, **item_data) 
    
        return sale

        