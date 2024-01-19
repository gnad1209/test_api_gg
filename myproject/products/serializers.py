from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from .models import Product
from rest_framework.validators import UniqueValidator

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


