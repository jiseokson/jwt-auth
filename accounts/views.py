from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from accounts.serializer import UserSerializer

User = get_user_model()

class AccountsInfo(APIView):
    allowed_methods = ('GET', 'POST')
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(pk=request.user.id) 
        return Response(UserSerializer(user).data)
    
    def post(self, request):
        serializer = UserSerializer(data=JSONParser().parse(request))
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(
            {
                'detail': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
            