from typing import Union
import requests

from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

User = get_user_model()

class OAuthTokenObtainView(APIView):

    allowed_methods = ('POST',)
    permission_classes = (AllowAny,)

    access_token_uri = {
        'github': 'https://github.com/login/oauth/access_token',
    }

    def get_client_id(self, provider: str) -> str:
        pass

    def get_client_secret(self, provider: str) -> str:
        pass

    def request_access_token(self, provider: str, access_code: str) -> dict:
        return requests.post(
            self.access_token_uri[provider],
            headers={
                'Accept': 'application/json'
            },
            params={
                'client_id': self.get_client_id(provider),
                'client_secret': self.get_client_secret(provider),
                'code': access_code,
            }
        ).json()
    
    def is_access_token_error(self, provider: str, response: dict) -> bool:
        return response.get('error') is not None
    
    def get_access_token_error(self, provider: str, response: dict) -> str:
        return response.get('error')
    
    def get_access_token(self, provider: str, response: dict) -> str:
        return response.get('access_token')
    
    def reqeust_email(self, provider, access_token) -> Union[str, None]:
        pass

    def post(self, request, provider: str) -> Response:
        # access code <-> access token 교환
        access_code = request.data.get('code')
        if access_code is None:
            return Response(
                {
                    'detail': 'Request data form is not valid',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        response = self.request_access_token(provider, access_code)
        if self.is_access_token_error(provider, response):
            return Response(
                {
                    'detail': self.get_access_token_error(provider, response)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        access_token = self.get_access_token(provider, response)

        # OAuth 제공 업체 provider에게 email 요청
        email = self.request_email(provider, access_token)
        if email is None:
            pass

        try:
            user = User.oauth_auths.get(email=email)
        except User.DoesNotExist as e:
            pass
            # 소셜 로그인으로 가입된 회원없으니 새로 가입 유도
            # return Response({ .. 회원가입으로 가랑 ..})
         
        # JWT 발급, 응답
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
        
