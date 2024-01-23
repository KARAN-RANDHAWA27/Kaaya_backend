from rest_framework import serializers
from .models import KaayaProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = KaayaProduct
        fields = '__all__'
