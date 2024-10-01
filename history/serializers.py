from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PurchaseHistory
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SaleHistory
        fields = '__all__'


class StatisticsSerializer(serializers.Serializer):
    total_products = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_sales = serializers.IntegerField()
    total_purchases = serializers.IntegerField()
    total_purchase_amount = serializers.IntegerField()
    total_sale_amount = serializers.IntegerField()
    total_suppliers = serializers.IntegerField()
    total_customers = serializers.IntegerField()