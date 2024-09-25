from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from . import models
from . import serializers
from history import models as sale_models
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


# class SaleViewSet(viewsets.ModelViewSet):
#     queryset = models.Sale.objects.all()
#     serializer_class = serializers.SaleSerializer
#     permission_classes = [permissions.AllowAny]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         self.perform_create(serializer)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         print("Validation Errors:", serializer.errors)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class SaleViewSet(viewsets.ModelViewSet):
    queryset = models.Sale.objects.all()
    serializer_class = serializers.SaleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def generate_purchase_code(self):
    #     return str(uuid.uuid4()).split('-')[0].upper()

    def generate_sale_code(self):
        return random.randint(100000, 999999)

    # def perform_create(self, serializer):
    #     generated_code = self.generate_purchase_code()
    #     sale = serializer.save(user=self.request.user, code=generated_code)
        
    #     # Create a single history entry
    #     sale_models.SaleHistory.objects.create(
    #         sale=sale,
    #         sale_code=sale.code,
    #         user=self.request.user,
    #         total_amount=sale.total_amount,
    #     )   

    def perform_create(self, serializer):
        generated_code = self.generate_sale_code()
        sale = serializer.save(user=self.request.user, code=generated_code)

        sale_history = sale_models.SaleHistory.objects.create(
            sale=sale,
            sale_code=sale.code,
            user=self.request.user,
            total_amount=sale.total_amount,
        ) 

        for item in sale.items.all():
            product = item.product
            # quantity = int(item.quantity)
            product.stock_quantity -= item.quantity  # Increase product stock by purchase quantity
            product.save()

    

