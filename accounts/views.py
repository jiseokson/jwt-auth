from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from accounts.serializer import UserSerializer

User = get_user_model()

class AccountsInfo(APIView):
    allowed_methods = ('GET',)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        access_token = request.headers.get('Authorization')[len('Bearer '):]
        payload = AccessToken(access_token).payload
        user = User.objects.get(pk=payload['user_id']) 
        return Response(UserSerializer(user).data)