from rest_framework import serializers
from .models import TblKaayaUserDetails

class GetUserDetails(serializers.ModelSerializer):
    class Meta:
        model = TblKaayaUserDetails
        fields = ['id', 'first_name', 'last_name', 'phone']