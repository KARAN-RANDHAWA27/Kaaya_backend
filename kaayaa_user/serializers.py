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
        fields = ['product', 'qty', 'user', 'created_date']