from django.db import models
# from .constants import UNIT
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

UNIT = (
    ('kg', 'kg'),
    ('gm', 'gm'),
    ('pc', 'pc'),
)
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    # image = models.ImageField( upload_to='images/products/', blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    description = models.TextField()
    product_quantity = models.IntegerField()
    unit = models.CharField( max_length=50, choices = UNIT)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)



    def __str__(self):
        return self.name