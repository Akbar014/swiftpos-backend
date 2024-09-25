from django.contrib import admin
from .models import Customer, Supplier, UserAccount
# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Supplier)
admin.site.register(Customer)