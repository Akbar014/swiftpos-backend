from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from . import models
from . import serializers

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
# token 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

# signals
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings

from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import ResetPasswordRequestToken



# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.AllowAny]

    # def perform_create(self, serializer):
    #     serializer.save()
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.UserAccount.objects.all()

    serializer_class = serializers.UserAccountSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # return super().get_queryset().filter(is_available_for_donation=True)
        return super().get_queryset()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Update using the UserAccountSerializer
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    


class UserRegistrationApiView(APIView): 
    serializer_class = serializers.RegistrationSerializer
    permission_classes = [permissions.AllowAny] 

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                token = default_token_generator.make_token(user)
               
                return Response("Successfully registered")
            except ValidationError as e:
                return Response(e.detail, status=400)
        return Response(serializer.errors, status=400)


class UserLoginApiView(APIView):
    permission_classes = [permissions.AllowAny] 
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                user = models.User.objects.get(username=username)
                if not user.is_active:
                    return Response({'error': "Please contact with super admin to active your account."}, status=403)
            except models.User.DoesNotExist:
                return Response({'error': "Invalid credentials."}, status=400)

            user = authenticate(username= username, password=password)
            if user:
                userAccount = models.UserAccount.objects.get(user=user)
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)

                return Response({'token' : token.key, 'user' : user.username, 'user_id' : userAccount.id, 'role' : userAccount.role})
            
            else:
                return Response({'error' : "Invalid Credential"})

        return Response(serializer.errors)


class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')



# password reset with django administration 
class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Send password reset email
        reset_url = f"http://127.0.0.1:8000/personapp/reset/{uid}/{token}/"
        subject = "Password Reset Request"
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return Response({'success': 'Password reset email sent'}, status=status.HTTP_200_OK)

# reset password with django rest password reset


class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    def post(self, request, *args, **kwargs):
        # Call the default behavior
        response = super().post(request, *args, **kwargs)
        
        # Get the token for the user
        email = request.data.get('email')
        
        # Get the token associated with the email
        if email:
            try:
                reset_password_token = ResetPasswordToken.objects.get(user__email=email)
                token = reset_password_token.key
                
                # Add the token to the response
                return Response({"status": "OK", "token": token}, status=status.HTTP_200_OK)
            except ResetPasswordToken.DoesNotExist:
                # If no token was created, return the default response
                return Response({"status": "OK", "message": "Token not found or not generated"}, status=status.HTTP_400_BAD_REQUEST)
        return response