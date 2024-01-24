from rest_framework import serializers
from .models import TblKaayaLogin

class AddLoginDetails(serializers.ModelSerializer):
    class Meta:
        model = TblKaayaLogin
        fields = ['id', 'username', 'usertype','is_email_verified','is_phone_verified']