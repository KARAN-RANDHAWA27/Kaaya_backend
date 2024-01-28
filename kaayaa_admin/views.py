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
from .models import TblKaayaAdminDetails
from .serializers import GetAdminDetails
from kaaya_login.models import TblKaayaLogin
from kaaya_login.serializers import DeleteLoginDetails
from rest_framework.pagination import PageNumberPagination


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
    
    def delete(self,request):
        success = False
        data = NULL
        message = ''
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            if request.user.usertype == 1:
                request.data._mutable = True
                if int(request.GET.get('vendor_id')):
                    try:
                        request.data['is_deleted'] = 1
                        request.data['is_active'] = 0
                        request.data['modified_by'] = request.user.id
                        request.data['modified_date'] = timezone.localtime(timezone.now())
                        vendorInstance = TblKaayaVendorDetails.objects.filter(id=request.GET.get('vendor_id'))
                        if vendorInstance:
                            vendornUser = TblKaayaLogin.objects.filter(id = vendorInstance.user)
                            deleteUser = DeleteLoginDetails(instance=vendornUser,data = request.data, partial =True)
                            if deleteUser.is_valid() and deleteUser.save():
                                vendorInstance.update(is_deleted = 1)
                                success = True
                                message = "Vendor deleted successfully"
                                data = ""
                                responseCode = status.HTTP_200_OK
                            else:
                                message = deleteUser.errors
                    except TblKaayaAdminDetails.DoesNotExist:
                        message = "Vendor doesn't exist"
                request.data._mutable = False
        except Exception as e:
            return Response({'success':success, 'data':data, 'message':e}, status=responseCode)
        return Response({'success':success, 'data':data, 'message':message}, status=responseCode)


class AllAdminView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Get all the admin list
    
    def post(self,request):
        success = False
        data = NULL
        message = ''
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        # Admin can add another
        try:
            if request.user.usertype == 1:
                request.data._mutable = True
                addAdmin = GetAdminDetails(request.data,partial = True)
                if addAdmin.is_valid() and addAdmin.save():
                    success = True
                    message = "Admin added succesfully"
                    data = addAdmin.data
                    responseCode = status.HTTP_201_CREATED
                else:
                    message = addAdmin.errors
                request.data._mutable = False
        except Exception as e:
            return Response({'success':success, 'data':data, 'message':e}, status=responseCode)
        return Response({'success':success, 'data':data, 'message':message}, status=responseCode)
    
    def delete(self,request):
        success = False
        data = NULL
        message = ''
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        # Admin can delete another admin
        try:
            if request.user.usertype == 1:
                request.data._mutable = True
                if int(request.GET.get('admin_id')) != 1:
                    try:
                        request.data['is_deleted'] = 1
                        request.data['is_active'] = 0
                        request.data['modified_by'] = request.user.id
                        request.data['modified_date'] = timezone.localtime(timezone.now())
                        adminInstance = TblKaayaAdminDetails.objects.filter(id=request.GET.get('admin_id'))
                        if adminInstance:
                            adminUser = TblKaayaLogin.objects.filter(id = adminInstance.user)
                            deleteUser = DeleteLoginDetails(instance=adminUser,data = request.data, partial =True)
                            if deleteUser.is_valid() and deleteUser.save():
                                success = True
                                message = "Admin deleted successfully"
                                data = ""
                                responseCode = status.HTTP_200_OK
                            else:
                                message = deleteUser.errors
                    except TblKaayaAdminDetails.DoesNotExist:
                        message = "Admin doesn't exist"
                request.data._mutable = False
        except Exception as e:
            return Response({'success':success, 'data':data, 'message':e}, status=responseCode)
        return Response({'success':success, 'data':data, 'message':message}, status=responseCode)
