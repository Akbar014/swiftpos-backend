from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from . import models
from . import serializers

from product import models as ProductModel
from sale import models as SaleModel
from purchase import models as PurchaseModel
from person import models as PersonModel
from django.db.models import Sum

# Create your views here.
class PurchaseHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.PurchaseHistory.objects.all()
    serializer_class = serializers.PurchaseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SaleHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.SaleHistory.objects.all()
    serializer_class = serializers.SaleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class StatisticsViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing statistics.
    """
    def list(self, request):
        # Aggregate the required statistics
        total_products = ProductModel.Product.objects.count()
        total_categories = ProductModel.Category.objects.count()
        total_sales = SaleModel.Sale.objects.count()
        total_purchases = PurchaseModel.Purchase.objects.count()

        total_purchase_amount = PurchaseModel.Purchase.objects.aggregate(Sum('total_amount'))['total_amount__sum']
        total_sale_amount = SaleModel.Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum']


        total_suppliers = PersonModel.Supplier.objects.count()
        total_customers = PersonModel.Customer.objects.count()

        # Prepare the data dictionary
        data = {
            'total_products': total_products,
            'total_categories': total_categories,
            'total_sales': total_sales,
            'total_purchases': total_purchases,
            'total_purchase_amount': total_purchase_amount,
            'total_sale_amount': total_sale_amount,
            'total_suppliers': total_suppliers,
            'total_customers': total_customers,
        }

        # Serialize the data
        serializer = serializers.StatisticsSerializer(data)
        return Response(serializer.data)

