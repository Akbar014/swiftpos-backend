from django.contrib import admin
from .models import Purchase, PurchaseItems
# Register your models here.
admin.site.register(Purchase)
admin.site.register(PurchaseItems)