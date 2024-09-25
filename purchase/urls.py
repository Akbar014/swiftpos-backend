from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 


router = DefaultRouter()
router.register('purchases', views.PurchaseViewSet)
# router.register('register', views.UserRegistrationApiView, basename='register')


urlpatterns = [
    
    path('', include(router.urls)),
     

]