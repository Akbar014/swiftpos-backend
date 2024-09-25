from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 
from django.contrib.auth import views as auth_views
from django_rest_passwordreset.views import ResetPasswordConfirm

router = DefaultRouter()
router.register('customer', views.CustomerViewSet, basename='customer')
router.register('supplier', views.SupplierViewSet, basename='supplier')
router.register('users', views.UserViewSet, basename='user')
# router.register('register', views.UserRegistrationApiView, basename='register')


urlpatterns = [

    path('', include(router.urls)),
    path('register/', views.UserRegistrationApiView.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

    # password reset with djsnor_rest_passwordreset
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/password_reset/', views.CustomResetPasswordRequestToken.as_view(), name='password_reset'),  
    # path('api/password_reset/confirm/', include('django_rest_passwordreset.urls', namespace='password_reset_confirm')),
     path('api/password_reset/confirm/', ResetPasswordConfirm.as_view(), name='password_reset_confirm'),

    
    # password reset with django administration 
    
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)