from django.db import models
from django.contrib.auth.models import User
# from person.models import Supplier 
from person import models as person_models
from product import models as product_models


# Create your models here.

class Purchase(models.Model):
    code = models.IntegerField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier = models.ForeignKey(person_models.Supplier, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    purchase_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Purchase {self.id} - {self.supplier}"

class PurchaseItems(models.Model):
    purchase = models.ForeignKey(Purchase,  related_name='items',  on_delete=models.CASCADE)
    product = models.ForeignKey(product_models.Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"

    

