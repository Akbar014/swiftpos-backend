from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from purchase import models as purchase_models
from sale import models as sale_models


class PurchaseHistory(models.Model):
    purchase = models.OneToOneField(purchase_models.Purchase, on_delete=models.CASCADE)
    purchase_code = models.IntegerField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Purchase by {self.user.username} on {self.date}"

class SaleHistory(models.Model):
    sale = models.OneToOneField(sale_models.Sale, on_delete=models.CASCADE)
    sale_code = models.IntegerField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"sales by {self.user.username} on {self.date}"
