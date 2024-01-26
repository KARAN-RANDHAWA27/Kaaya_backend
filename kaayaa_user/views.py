from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from pymysql import NULL
from django.utils import timezone
from kaayaa_user.serializers import GetUserDetails, CartSerializer
from kaaya_login.serializers import AddLoginDetails
from django.contrib.auth.hashers import make_password
from .models import CartItem
from django.core.exceptions import ValidationError
from django.db.models import Q

class UserRegisterView(APIView):
    def post(self, request):
        success = False
        data = NULL
        message = ''
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            requestPayload = {
                'created_date': timezone.localtime(timezone.now()),
                'usertype': 3,
                'username': request.data['username'],
                'password': make_password(request.data['password'])
            }
            addUserLogin = AddLoginDetails(data=requestPayload)
            
            if addUserLogin.is_valid() and addUserLogin.save():
                userData = {
                    "user":  addUserLogin.data['id'],
                    "first_name": request.data['first_name'],
                    "last_name": request.data['last_name'],
                    "phone": request.data['phone'],
                }
                addUserData = GetUserDetails(data=userData)
                
                if addUserData.is_valid() and addUserData.save():
                    success = True
                    data = addUserData.data
                    message = "User added Successfully"
                    responseCode = status.HTTP_201_CREATED
                else:
                    message = addUserData.errors
            else:
                    message = addUserLogin.errors
            
        except Exception as e:
           return Response({'success': success, 'data': data, 'message': str(e)}, status=responseCode)
        
        return Response({'success':success, 'data':data, 'message':message}, status=responseCode)
    
    
class CartOperations(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    # Add to cart
    def post(self, request): 
        success = False
        data = None
        message = ''
        responseCode = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        try:
            print(request.user)
            user_type = request.user.usertype

            if user_type != 3:
                raise ValidationError("Invalid User!!!")

            # Check if the user already has the same product in the cart
            product_id = request.data.get('product', None)
            if product_id is not None:
                existing_cart_item = CartItem.objects.filter(
                    Q(user=request.user) & Q(product=product_id)
                ).first()
                if existing_cart_item:
                    raise ValidationError("Product already exists in the user's cart.")

            cart_serializer = CartSerializer(data=request.data)

            if cart_serializer.is_valid():
                cart_instance = cart_serializer.save(user=request.user)  # Associate the cart item with the current user
                success = True
                data = {'cart_id': cart_instance.id}
                message = 'Product added to the cart successfully'
                responseCode = status.HTTP_201_CREATED
            else:
                message = cart_serializer.errors
            
        except ValidationError as ve:
            message = str(ve)
            responseCode = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return Response({'success': success, 'data': data, 'message': str(e)}, status=responseCode)
        
        return Response({'success': success, 'data': data, 'message': message}, status=responseCode)
    
    
    # Update Cart Details
    def patch(self, request, cart_id):
        success = False
        data = None
        message = ''
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        try:
            cart_instance = CartItem.objects.get(id=cart_id)
            
            cart_serializer = CartSerializer(cart_instance, data=request.data, partial=True)
            
            if cart_serializer.is_valid() and cart_serializer.save():
                success = True
                data = {'cart_id': cart_instance.id}
                message = 'Cart item quantity updated successfully'
                response_code = status.HTTP_200_OK
            else:
                message = cart_serializer.errors

        except CartItem.DoesNotExist:
            message = 'Cart item not found'
            response_code = status.HTTP_404_NOT_FOUND
        except Exception as e:
            return Response({'success': success, 'data': data, 'message': str(e)}, status=response_code)

        return Response({'success': success, 'data': data, 'message': message}, status=response_code)
        
        
