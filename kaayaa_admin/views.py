from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from pymysql import NULL
from django.utils import timezone
from kaaya_login.serializers import AddLoginDetails
from kaayaa_vendor.models import TblKaayaVendorDetails
from kaayaa_vendor.serializers import GetVendorDetails

class AllVendorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Get all the vendor list for admin
    def get(self,request):
        success = False
        data = NULL
        message = ''
        vendorData = {}
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            if request.user.usertype == 1:
                if request.GET.get('is_pending'):
                    vendorData = TblKaayaVendorDetails.objects.filter(is_approved = 0,is_deleted = 0)
                else:
                    vendorData = TblKaayaVendorDetails.objects.filter(is_approved = 1,is_deleted = 0)
                if vendorData:
                    allVendorData = GetVendorDetails(vendorData,many=True)
                    data = allVendorData.data
                    success = True
                    message = "Vendor data retrieved successfully"
                    responseCode = status.HTTP_200_OK
                else:
                    message = "Vendor data doesn't exist"
                    success = True
                    responseCode = status.HTTP_200_OK
        except Exception as e:
            return Response({'success':success, 'data':data, 'message':e}, status=responseCode)
        return Response({'success':success, 'data':data, 'message':message}, status=responseCode)
    
    def post(self,request):
        success = False
        data = NULL
        message = ''
        vendorData = {}
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        # Approve vendor by admin
        try:
            if request.user.usertype == 1:
                if request.GET.get('vendor_id'):
                    vendor_instance = TblKaayaVendorDetails.objects.filter(id= request.GET.get('vendor_id'))
                    if vendor_instance:
                        vendor_instance.update(is_approved = 1,approved_by= request.user.id,approved_date = timezone.localtime(timezone.now()))
                        vendor_id = vendor_instance['user']
                        # Get the email from the TblKaayaLogin using vendor id and send a mail to verify  
                        # Send mail to vendor
                        success = True
                        message = "Vendor approved successfully"
                        responseCode = status.HTTP_200_OK
                    else:
                        message = "Vendor update failed"
        except Exception as e:
            return Response({'success':success, 'data':data, 'message':e}, status=responseCode)
        return Response({'success':success, 'data':data, 'message':message}, status=responseCode)


