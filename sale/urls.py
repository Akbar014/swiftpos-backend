from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 




router = DefaultRouter()
router.register('sales', views.SaleViewSet)
# router.register('register', views.UserRegistrationApiView, basename='register')


urlpatterns = [
    
    path('', include(router.urls)),
    path('sales_with_online_payment/', views.salePayment),
    
    path('success_payment/<str:username>/<str:tran_id>/<int:customer>/<int:discount>/success', views.payment_success),
     
]