from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from accounts.serializer import UserSerializer

User = get_user_model()

class AccountsInfo(APIView):
    allowed_methods = ('GET', 'POST')
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(pk=request.user.get('user_id')) 
        return Response(UserSerializer(user).data)
    
    def post(self, request):
        user = User.objects.get(pk=request.user.get('user_id'))
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.is_active = True
        user.save()
        return Response(UserSerializer(user).data)