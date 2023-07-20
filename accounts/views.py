from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.serializer import UserRegistSerializer, UserSerializer

User = get_user_model()

class AccountsInfo(APIView):
    allowed_methods = ('GET', 'POST')
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(UserSerializer(request.user).data)
    
    def post(self, request):
        user = request.user
        data = request.data

        register_serializer = UserRegistSerializer(user, data=data, partial=True)
        if not register_serializer.is_valid():
            return Response(
                {
                    **register_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        register_serializer.save(is_register=True)
        return Response(UserSerializer(user).data)