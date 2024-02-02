from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer,ProductCategorySerializer
from .models import KaayaProduct
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from django.utils import timezone
from .models import KaayaProduct,KaayaaProductsCategory

class ProductsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        success = False
        data = None
        message = None
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        try:
            if request.user.usertype == 2:
                if request.GET.get('product_id'):
                    product_instance = KaayaProduct.objects.filter(id= int(request.GET.get('product_id')))
                    serializer = ProductSerializer(instance=product_instance, data=request.data,partial=True)
                    if serializer.is_valid() and serializer.save():
                        success = True
                        data = serializer.data
                        message = 'Product updated successfully'
                        response_code = status.HTTP_200_OK
                else:
                    request.data._mutable = True
                    request.data['is_approved'] = 0
                    request.data['approved_by'] = 0
                    serializer = ProductSerializer(data=request.data,partial=True)
                    if serializer.is_valid() and serializer.save():
                        success = True
                        data = serializer.data
                        message = 'Product added successfully'
                        response_code = status.HTTP_201_CREATED
                    else:
                        message = serializer.errors
                    request.data._mutable = False
        except Exception as e:
            message = e
            return Response({'success': success, 'data': data, 'message': message}, status=response_code)
        
        return Response({'success': success, 'data': data, 'message': message}, status=response_code)

    
    def get(self, request): 
        success = False
        data = None
        message = None
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            products = KaayaProduct.objects.all()
            serializer= ProductSerializer(products,many=True)
            
            if serializer.data:
                success = True
                data = serializer.data
                message = "Products data retrieved successfully"
                response_code = status.HTTP_200_OK
            else:
                success = True
                message = "No product found"
                response_code = status.HTTP_200_OK
            return Response({'success': success, 'data': data, 'message': message},status=response_code)
        except Exception as e:
            message = 'Products data retrieved failed'
            return Response({'success': success, 'data': data, 'message': message}, status=response_code)
        
    def delete(self,request):
        success = False
        data = None
        message = None
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            if request.user.usertype == 2 or request.user.usertype == 1:
                if request.GET.get('product_id'):
                    request.data._mutable = True
                    request.data['modified_by'] = request.user.id
                    request.data['modified_at'] = timezone.localtime(timezone.now())
                    request.data['is_deleted'] = 1
                    product_instance = KaayaProduct.objects.filter(id= int(request.GET.get('product_id')))
                    serializer = ProductSerializer(instance=product_instance, data=request.data,partial=True)
                    if serializer.is_valid() and serializer.save():
                        success = True
                        data = serializer.data
                        message = 'Product deleted successfully'
                        response_code = status.HTTP_200_OK
                    else:
                        message = 'Product deletion failed'
                    request.data._mutable = False
        except Exception as e:
            message = e
            return Response({'success': success, 'data': data, 'message': message}, status=response_code)
        return Response({'success': success, 'data': data, 'message': message}, status=response_code)
    

class CategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        success = False
        data = None
        message = None
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        try:
            if request.user.usertype == 2:
                if request.GET.get('category_id'):
                    category_instance = KaayaaProductsCategory.objects.filter(id= int(request.GET.get('category_id')))
                    serializer = ProductCategorySerializer(instance=category_instance, data=request.data,partial=True)
                    if serializer.is_valid() and serializer.save():
                        success = True
                        data = serializer.data
                        message = 'Category updated successfully'
                        response_code = status.HTTP_200_OK
                else:
                    request.data._mutable = True
                    request.data['is_approved'] = 0
                    request.data['approved_by'] = 0
                    serializer = ProductCategorySerializer(data=request.data,partial=True)
                    if serializer.is_valid() and serializer.save():
                        success = True
                        data = serializer.data
                        message = 'Category added successfully'
                        response_code = status.HTTP_201_CREATED
                    else:
                        message = serializer.errors
                    request.data._mutable = False
        except Exception as e:
            message = e
            return Response({'success': success, 'data': data, 'message': message}, status=response_code)
        
        return Response({'success': success, 'data': data, 'message': message}, status=response_code)

    
    def get(self, request): 
        success = False
        data = None
        message = None
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            categories = KaayaaProductsCategory.objects.all()
            serializer= ProductCategorySerializer(categories,many=True)
            
            if serializer.data:
                success = True
                data = serializer.data
                message = "Category data retrieved successfully"
                response_code = status.HTTP_200_OK
            else:
                message = "Category data retrieved failed"
            return Response({'success': success, 'data': data, 'message': message},status=response_code)
        except Exception as e:
            return Response({'success': success, 'data': data, 'message': message}, status=response_code)
        
    def delete(self,request):
        success = False
        data = None
        message = None
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            if request.user.usertype == 2 or request.user.usertype == 1:
                if request.GET.get('category_id'):
                    request.data._mutable = True
                    request.data['modified_by'] = request.user.id
                    request.data['modified_at'] = timezone.localtime(timezone.now())
                    request.data['is_deleted'] = 1
                    category_instance = KaayaaProductsCategory.objects.filter(id= int(request.GET.get('product_id')))
                    serializer = ProductCategorySerializer(instance=category_instance, data=request.data,partial=True)
                    if serializer.is_valid() and serializer.save():
                        success = True
                        data = serializer.data
                        message = 'Category deleted successfully'
                        response_code = status.HTTP_200_OK
                    else:
                        message = 'Category deletion failed'
                    request.data._mutable = False
        except Exception as e:
            message = e
            return Response({'success': success, 'data': data, 'message': message}, status=response_code)
        return Response({'success': success, 'data': data, 'message': message}, status=response_code)