from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 


router = DefaultRouter()
router.register('purchaseHistory', views.PurchaseHistoryViewSet)
router.register('saleHistory', views.SaleHistoryViewSet)
router.register('statistics', views.StatisticsViewSet, basename='statistics')
# router.register('register', views.UserRegistrationApiView, basename='register')


urlpatterns = [
    
    path('', include(router.urls)),
     

]