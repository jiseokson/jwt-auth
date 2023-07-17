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
        user = User.objects.get(pk=request.user.id) 
        return Response(UserSerializer(user).data)
    
    def post(self, request):
        user = request.user
        user.name = request.data.get('name')
        user.phone = request.data.get('phone')
        user.univ = request.data.get('univ')
        user.student_id = request.data.get('student_id')
        user.track = request.data.get('track')
        user.is_register = True
        user.save()
        return Response(UserSerializer(user).data)