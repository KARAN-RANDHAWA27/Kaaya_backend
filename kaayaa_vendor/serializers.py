from rest_framework import serializers
from .models import TblKaayaVendorDetails

class GetVendorDetails(serializers.ModelSerializer):
    class Meta:
        model = TblKaayaVendorDetails
        fields = ['id', 'user','first_name', 'last_name', 'phone','is_approved','approved_by','approved_date']