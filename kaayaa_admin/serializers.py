from rest_framework import serializers
from .models import TblKaayaAdminDetails

class GetAdminDetails(serializers.ModelSerializer):
    class Meta:
        model = TblKaayaAdminDetails
        fields = ['id', 'first_name', 'last_name', 'phone']
