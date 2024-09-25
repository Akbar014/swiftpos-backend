from django.db import models
from django.contrib.auth.models import User
from person import models as person_models
from product import models as product_models

# Create your models here.

class Sale(models.Model):
    code = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(person_models.Customer, on_delete=models.CASCADE)
    discount = models.IntegerField()
    total_amount = models.IntegerField()
    sale_date = models.DateField( auto_now_add=True)

    def __str__(self):
        return f"Sale {self.id} - {self.customer} {self.code}"

class SaleItems(models.Model):
    sale = models.ForeignKey(Sale,  related_name='items',  on_delete=models.CASCADE)
    product = models.ForeignKey(product_models.Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"