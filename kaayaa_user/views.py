from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from pymysql import NULL
from django.utils import timezone
from kaaya_login.serializers import AddLoginDetails


class VendorRegisterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        success = False
        data = NULL
        message = ''
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            request.data._mutable = True
            request.data['created_date'] = timezone.localtime(timezone.now())
            request.data['usertype'] = 2
            request.data['is_email_verified'] = 0
            request.data['is_phone_verified'] = 0
            
            request.data._mutable = False
        except Exception as e:
            return Response({'success':success, 'data':data, 'message':e}, status=responseCode)
        return Response({'success':success, 'data':data, 'message':message}, status=responseCode)