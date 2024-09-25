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
