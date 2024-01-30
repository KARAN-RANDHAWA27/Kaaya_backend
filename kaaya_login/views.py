from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymysql import NULL
from .models import TblKaayaLogin
from django.db.models import Q
from django.contrib.auth.hashers import check_password,make_password
from kaaya_backend.settings import EXPIRY_TIME
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from kaayaa_admin.models import TblKaayaAdminDetails
from kaayaa_vendor.models import TblKaayaVendorDetails
from kaayaa_user.models import TblKaayaUserDetails
from kaayaa_admin.serializers import GetAdminDetails
from kaayaa_user.serializers import GetUserDetails
from kaayaa_vendor.serializers import GetVendorDetails

class KaayaaLoginUser(APIView):
    def post(self, request):
        print("he")
        success = False
        data = None
        message = None
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            username = request.data['username'].strip()
            password = request.data['password'].strip()
            login_user = TblKaayaLogin.objects.get(Q(username=username), Q(
                is_email_verified='1', is_phone_verified='1'), Q(is_deleted='0'), Q(is_active='1'))
            userType = login_user.usertype
            if login_user:
                matchcheck = check_password(
                    password, login_user.password)  # matching encrypted password through check password module
                if matchcheck:
                    refresh = RefreshToken.for_user(login_user)
                    print(login_user)
                    success = True
                    access_token = str(refresh.access_token)
                    data = {'refresh': str(refresh), 'access': access_token, 'userType': str(userType),
                            'expiryTime': int(EXPIRY_TIME)}
                    message = 'logged in successfully'
                    responseCode = status.HTTP_200_OK
                else:
                    message = 'Username or password is wrong'

        except TblKaayaLogin.DoesNotExist:
            message = 'Username or password is wrong'
            responseCode = status.HTTP_401_UNAUTHORIZED
        except Exception as e:
            message = 'Internal server error'
            print(e)

        return Response({'success': success, 'data': data, 'message': message}, status=responseCode)


class Profile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  
# Based on the usertype get the data of the user.
    def get(self, request):
        success = False
        data = NULL
        message = NULL
        loginDetails = {}
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            if request.user.usertype == 1:
                kaayaaUserDetail = TblKaayaAdminDetails.objects.get(
                    user=request.user.id)
                loginDetails = GetAdminDetails(kaayaaUserDetail)
            elif request.user.usertype == 2:
                kaayaaUserDetail = TblKaayaVendorDetails.objects.get(
                    user=request.user.id)
                loginDetails = GetVendorDetails(kaayaaUserDetail)
            elif request.user.usertype == 3:
                kaayaaUserDetail = TblKaayaUserDetails.objects.get(
                    user=request.user.id)
                loginDetails = GetUserDetails(kaayaaUserDetail)
            if loginDetails.data:
                success = True
                data = loginDetails.data
                message = 'Profile retrieved successfully'
                responseCode = status.HTTP_200_OK
            else:
                message = 'Profile retrieved failed'
                data = ""
        except Exception as e:
            print(e)
        return Response({'success': success, 'data': data, 'message': message}, status=responseCode)


class Logout(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        success = False
        data = NULL
        message = NULL
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            success = True
            data = NULL
            message = "logged out successfully"
            responseCode = status.HTTP_200_OK
        except Exception as e:
            message = 'logout failed'
        return Response({'success': success, 'data': data, 'message': message}, status=responseCode)