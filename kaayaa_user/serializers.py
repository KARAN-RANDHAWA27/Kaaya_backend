from rest_framework import serializers
from .models import TblKaayaUserDetails, CartItem
from kaaya_products.models import KaayaProduct

class GetUserDetails(serializers.ModelSerializer):
    class Meta:
        model = TblKaayaUserDetails
        fields = ['user', 'first_name', 'last_name', 'phone']
        
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def validate_product(self, value):
        try:
            product = KaayaProduct.objects.get(id=value)
        except KaayaProduct.DoesNotExist:
            raise serializers.ValidationError("Invalid product ID. Product does not exist.")
        return value