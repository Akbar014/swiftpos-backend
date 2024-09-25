from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from product import models as product_models


class PurchaseItemsSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=product_models.Product.objects.all())

    class Meta:
        model = models.PurchaseItems
        fields = ['product', 'quantity', 'unit_price']

    


class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemsSerializer(many=True)
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.Purchase
        fields = ['id', 'code', 'user', 'supplier', 'total_amount', 'purchase_date', 'items']

    

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        purchase = models.Purchase.objects.create(**validated_data)

        # Check if the purchase instance is created correctly
        print("Created Purchase:", purchase)

        # Validate and create PurchaseItems
        for item_data in items_data:
            # item_serializer = PurchaseItemsSerializer(data=item_data)
            # if item_serializer.is_valid():
            #     item_serializer.save(purchase=purchase)
            # else:
            #     print("Item Errors:", item_serializer.errors)
            #     raise serializers.ValidationError(item_serializer.errors)
            models.PurchaseItems.objects.create(purchase=purchase, **item_data) 
    
        return purchase

       