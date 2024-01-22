from rest_framework import serializers
from .models import TblKaayaVendorDetails

class GetVendorDetails(serializers.ModelSerializer):
    class Meta:
        model = TblKaayaVendorDetails
        fields = ['id', 'first_name', 'last_name', 'phone']