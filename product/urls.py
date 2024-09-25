from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 


router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='products' )
router.register('category', views.CategoryViewSet, basename='category')
# router.register('register', views.UserRegistrationApiView, basename='register')


urlpatterns = [
    path('', include(router.urls)),
    # path('productsapp/', include(router.urls)),
     

]
