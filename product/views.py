from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from product import models, serializers

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
        
    #     # If 'image' is not in the request data, keep the current image
    #     if 'image' not in request.data:
    #         request.data['image'] = instance.image

    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
   
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.AllowAny]