from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.
roles = (
    ('admin', 'admin'),
    ('manager', 'manager'),
    ('cashier', 'cashier'),
)

class UserAccount(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    role = models.CharField(max_length=50, choices= roles )
    # image = models.ImageField( upload_to='person/images/', blank=True, null=True)
    image = CloudinaryField('image')
    phone = models.CharField( max_length=20,  blank= True, null= True)
    address = models.CharField(max_length=100, blank= True, null= True)

class Supplier (models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank= True, null= True)
    phone = models.CharField( max_length=20)
    address = models.TextField(blank=True, null= True)

    def __str__(self):
        return self.name
    
    
class Customer (models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField( max_length=20)
    address = models.TextField(blank=True, null= True)

    def __str__(self):
        return self.name

