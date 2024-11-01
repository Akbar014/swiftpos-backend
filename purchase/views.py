from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from . import models
from . import serializers
from history import models as purchase_models
import random
import uuid
# Create your views here.
# class PurchaseViewSet(viewsets.ModelViewSet):
    
#     queryset = models.Purchase.objects.all()
#     serializer_class = serializers.PurchaseSerializer
#     permission_classes = [permissions.AllowAny]

# class PurchaseItemsViewSet(viewsets.ModelViewSet):
   
#     queryset = models.PurchaseItems.objects.all()
#     serializer_class = serializers.PurchaseItemsSerializer
#     permission_classes = [permissions.AllowAny]


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = models.Purchase.objects.all().order_by('-id')
    serializer_class = serializers.PurchaseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    
    def generate_purchase_code(self):
        return random.randint(100000, 999999)

    def perform_create(self, serializer):
        generated_code = self.generate_purchase_code()
        purchase = serializer.save(user=self.request.user, code=generated_code)

        purchase_history = purchase_models.PurchaseHistory.objects.create(
            purchase=purchase,
            purchase_code=purchase.code,
            user=self.request.user,
            total_amount=purchase.total_amount,
        ) 

        for item in purchase.items.all():
            product = item.product
            # quantity = int(item.quantity)
            product.stock_quantity += item.quantity  # Increase product stock by purchase quantity
            product.save()
        
        # Create a single history entry
          

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def generate_purchase_code(self):
    #     return str(uuid.uuid4()).split('-')[0].upper()


