from typing import Union
import requests

from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from accounts.managers import OAUTH_PROVIDER

User = get_user_model()

class OAuthTokenObtainView(APIView):

    allowed_methods = ('POST',)
    permission_classes = (AllowAny,)

    access_token_uri = {
        'github': 'https://github.com/login/oauth/access_token',
    }

    email_uri = {
        'github': 'https://api.github.com/user/emails',
    }

### SECRET ###
    client_id = {
        'github': '9b1df8c5638f9aab5523',
    }

### SECRET ###
    client_secret = {
        'github': 'c00b4a7450430a65f2bbc90bfcac0d5cd85aa8d9'
    }

    def request_access_token(self, provider: str, access_code: str) -> dict:
        if provider == 'github':
            return requests.post(
                self.access_token_uri[provider],
                headers={
                    'Accept': 'application/json'
                },
                params={
                    'client_id': self.client_id[provider],
                    'client_secret': self.client_secret[provider],
                    'code': access_code,
                }
            ).json()
    
    def is_access_token_error(self, provider: str, response: dict) -> bool:
        if provider == 'github':
            return response.get('error') is not None
    
    def get_access_token_error(self, provider: str, response: dict) -> str:
        if provider == 'github':
            return response.get('error')
    
    def get_access_token(self, provider: str, response: dict) -> str:
        if provider == 'github':
            return response.get('access_token')
    
    def reqeust_email(self, provider, access_token) -> Union[str, None]:
        if provider == 'github':
            emails = requests.get(
                self.email_uri[provider],
                headers={
                    'Authorization': f'Bearer {access_token}'
                }
            ).json()
            return next(email for email in emails if email['primary'])

    def post(self, request, provider: str) -> Response:
        # OAuth 제공 업체 이름의 유효성 검사
        if provider not in OAUTH_PROVIDER:
            return Response(
                {
                'detail': 'Invalid Provider'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
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

        # 인증된 email로 사용자 정보 탐색
        try:
            user = User.oauths.get(email=email)
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
        
