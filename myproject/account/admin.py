from django.contrib import admin
from .models import Product,CustomUser
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)