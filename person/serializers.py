from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class CustomerSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(many=False)
    
    class Meta:
        model = models.Customer
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(many=False)
    
    class Meta:
        model = models.Supplier
        fields = '__all__'

roles = [
    ('admin', 'admin'),
    ('manager', 'manager'),
    ('cashier', 'cashier'),
]

class RegistrationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices= roles )
    image = serializers.ImageField( required=False )
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'phone', 'role', 'image', 'address', 'password', 'confirm_password']
        # fields =  '__all__'

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        is_active = self.validated_data['is_active']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        role = self.validated_data['role']
        address = self.validated_data['address']
        phone = self.validated_data['phone']
        image = self.validated_data.get('image') 

        if password != password2:
            raise serializers.ValidationError({'error': "Passwonrd Doesn't Matched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email Already Exists'})

        user = User(username = username, email=email, first_name = first_name, last_name = last_name, is_active=is_active)
       
        user.set_password(password)
        # user.is_active = False
        user.save()

        models.UserAccount.objects.create(
            user = user,
            phone = phone,
            address = address,
            role = role,
            image = image,

        )

        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)


# roles = [

#     ('admin', 'admin'),
#     ('manager', 'manager'),
#     ('cashier', 'cashier'),
# ]

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__' 
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
    

class UserAccountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    is_active = serializers.BooleanField(source='user.is_active', required=False)
    

    # fields from userAccount model
    role = serializers.ChoiceField(choices=roles) 
    image = serializers.ImageField(allow_null=True, required=False)
    # phone = models.CharField( max_length=20,  blank= True, null= True)
    phone = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = models.UserAccount
        fields = [
             'id', 'username', 'first_name', 'last_name', 'email', 'role',  'image', 'phone', 'address', 'is_active',
        ]

    def create(self, validated_data):
        
        user_data = validated_data.pop('user',{})
        user = User.objects.create(**user_data)

        user_account = models.UserAccount.objects.create(user=user, **validated_data)
        return user_account

    def update(self, instance, validated_data):
        # Handle nested user update
        print(validated_data)
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        # Handle UserAccount update
        return super().update(instance, validated_data)


