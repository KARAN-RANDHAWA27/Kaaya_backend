from django.shortcuts import get_object_or_404
from django.http import Http404
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
from .models import CartItem, KaayaProduct, TblKaayaUserDetails
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

    def _validate_user_and_product(self, user, product_id, usertype):
        if usertype != 3:
            raise ValidationError("Invalid user.")

        existing_cart_item = CartItem.objects.filter(user=user, product=product_id).first()
        if existing_cart_item:
            raise ValidationError("Product already exists in the user's cart.")

    # Add to cart
    def post(self, request):
        success = False
        data = None
        message = ''
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        try:
            user = request.user
            product_id = request.data.get('product')
            qty = request.data.get('qty')
            usertype = request.user.usertype
            
            user_instance = get_object_or_404(TblKaayaUserDetails, user=user.id)

            self._validate_user_and_product(user_instance.id, product_id, usertype)

            product_instance = get_object_or_404(KaayaProduct, id=product_id)
            
            cart_serializer = CartSerializer(data={
                'product': product_instance.id,
                'qty': qty,
                'user': user_instance.id,
                'created_date': timezone.now()
            }, partial=True)

            if qty > product_instance.qty:
                raise ValidationError("Quantity exceeds available stock.")

            if cart_serializer.is_valid():
                cart_instance = cart_serializer.save()
                success = True
                data = {'cart_id': cart_instance.id}
                message = 'Product added to the cart successfully'
                response_code = status.HTTP_201_CREATED
            else:
                message = cart_serializer.errors

        except ValidationError as ve:
            message = str(ve)
            response_code = status.HTTP_400_BAD_REQUEST
        except Http404:
            message = 'User or product not found'
            response_code = status.HTTP_404_NOT_FOUND
        except Exception as e:
            return Response({'success': success, 'data': data, 'message': str(e)}, status=response_code)

        return Response({'success': success, 'data': data, 'message': message}, status=response_code)


    # Update Cart Details
    def patch(self, request, cart_id):
        success = False
        data = None
        message = ''
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        try:
            new_qty = request.data.get('qty')
            usertype = request.user.usertype
            
            if usertype != 3:
                raise ValidationError("Invalid user.")
            
            if not isinstance(new_qty, int): 
                raise ValidationError('Quantity Not Found')

            if new_qty <= 0:
                raise ValidationError("Quantity must be greater than zero.")
            
            cart_instance = CartItem.objects.get(id=cart_id)
            product_instance = KaayaProduct.objects.get(id = cart_instance.product.id)
            
            if product_instance.qty < new_qty:
                raise ValidationError("Quantity exceeds.")
            
            cart_instance.qty = new_qty
            cart_instance.save()

            success = True
            data = {'cart_id': cart_instance.id}
            message = 'Cart item quantity updated successfully'
            response_code = status.HTTP_200_OK

        except CartItem.DoesNotExist:
            message = 'Cart item not found'
            response_code = status.HTTP_404_NOT_FOUND
        except KaayaProduct.DoesNotExist:
            message = 'Product not found'
            response_code = status.HTTP_404_NOT_FOUND
        except ValidationError as ve:
            message = str(ve)
            response_code = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return Response({'success': success, 'data': data, 'message': str(e)}, status=response_code)

        return Response({'success': success, 'data': data, 'message': message}, status=response_code)