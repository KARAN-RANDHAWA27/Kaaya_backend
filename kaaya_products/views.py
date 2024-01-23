from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework import generics
from .models import KaayaProduct

class ProductsView(generics.ListCreateAPIView):
    queryset = KaayaProduct.objects.all()
    serializer_class = ProductSerializer
    
    def post(self, request):
        success = False
        data = None
        message = None
        response_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                product_instance = serializer.save()

                success = True
                data = {'id': product_instance.id}
                message = 'Product added successfully'
                response_code = status.HTTP_201_CREATED
            else:
                message = serializer.errors
        except Exception as e:
            message = 'Internal server error'
            print(e)
        
        return Response(
            {'success': success, 'data': data, 'message': message}, 
            status=response_code
        )
    
    def get(self, request): 
        try:
            queryset = self.get_queryset()
            
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({'success': True, 'data': serializer.data, 'message': 'Products retrieved successfully'})
        except Exception as e:
            return Response({'success': False, 'data': None, 'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
