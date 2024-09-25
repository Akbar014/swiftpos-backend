from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from . import models
from . import serializers


# Create your views here.
class PurchaseHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.PurchaseHistory.objects.all()
    serializer_class = serializers.PurchaseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SaleHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.SaleHistory.objects.all()
    serializer_class = serializers.SaleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

