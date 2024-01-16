from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from .models import CustomUser,Product,BlacklistedToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

#todo
class BlacklistedTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlacklistedToken
        fields = '__all__'


class LogoutSerializers(serializers.ModelSerializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expried or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs
    
    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')