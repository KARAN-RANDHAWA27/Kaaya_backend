from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelloAPIView(APIView):
    def get(self, request):
        print("hey")
        return Response({'message': 'Hello, World!'}, status=status.HTTP_200_OK)