from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from kaaya_backend.settings import EXPIRY_TIME
# from rest_framework.response import Res

class RefreshTokensSerializer(TokenRefreshSerializer):
    @classmethod
    def validate(cls, attrs):
        try:
            tokenMaster = super().validate(cls, attrs)
            
            token = {}
            token['success'] = True
            token['data'] = tokenMaster
            token['data']['expiryTime'] = EXPIRY_TIME
            token['message'] = 'Token retrieved successfully'
            return token
        except Exception as e:
            token = {}
            token['success'] = False
            token['data'] = {}
            token['data']['expiryTime'] = 0
            token['message'] = 'Token not retrived'
            return token  

class MyTokenObtainPairView(TokenRefreshView):
    serializer_class = RefreshTokensSerializer