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

    redirect_uri = {
        'github': 'http://localhost:3000/githubCallback',
        'kakao': 'http://localhost:3000/kakaoCallback',
        'google': 'http://localhost:3000/googleCallback'
    }

    access_token_uri = {
        'github': 'https://github.com/login/oauth/access_token',
        'kakao': 'https://kauth.kakao.com/oauth/token',
        'google': 'https://oauth2.googleapis.com/token'
    }

    email_uri = {
        'github': 'https://api.github.com/user/emails',
        'kakao': 'https://kapi.kakao.com/v2/user/me',
        'google': 'https://www.googleapis.com/oauth2/v1/userinfo'
    }

### SECRET ###
    client_id = {
        'github': '9b1df8c5638f9aab5523',
        'kakao': 'c98455cce815417ca28f9a973d9a24a7',
        'google': '374838732950-m9o6ik80g35uf9j7u7mh5jrhatl8869n.apps.googleusercontent.com',
    }

### SECRET ###
    client_secret = {
        'github': 'c00b4a7450430a65f2bbc90bfcac0d5cd85aa8d9',
        'kakao': '',
        'google': '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',
    }

### Todo: 보안을 위해 값을 숨길 것
    def get_client_id(self, provider):
        return self.client_id[provider]
    
    def get_client_secret(self, provider):
        return self.client_secret[provider]

    def request_access_token(self, provider: str, access_code: str) -> dict:
        if provider == 'github':
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
        elif provider == 'kakao':
            return requests.post(
                self.access_token_uri[provider],
                headers={
                    'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
                },
                data={
                    'grant_type': 'authorization_code',
                    'client_id': self.get_client_id(provider),
                    'redirect_uri': self.redirect_uri[provider],
                    'code': access_code,
                }
            ).json()
        elif provider == 'google':
            return requests.post(
                self.access_token_uri[provider],
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data={
                    'grant_type': 'authorization_code',
                    'client_id': self.get_client_id(provider),
                    'client_secret': self.get_client_secret(provider),
                    'redirect_uri': self.redirect_uri[provider],
                    'code': access_code,
                }
            ).json()
    
    def is_access_token_error(self, provider: str, response: dict) -> bool:
        # !!! google의 에러코드 확인된 적 없음
        if provider in ('github', 'kakao', 'google',):
            return response.get('error') is not None
    
    def get_access_token_error(self, provider: str, response: dict) -> str:
        # !!! google의 에러코드 확인된 적 없음
        if provider in ('github', 'kakao', 'google',):
            return response.get('error')
    
    def get_access_token(self, provider: str, response: dict) -> str:
        if provider in ('github', 'kakao', 'google',):
            return response.get('access_token')
    
    def reqeust_email(self, provider, access_token) -> Union[str, None]:
        return requests.get(
            self.email_uri[provider],
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        ).json()

    def get_email(self, provider, response):
        if provider == 'github':
            # primary가 없는 경우 존재..??
            return next(email for email in response if email['primary']).get('email')
        elif provider == 'kakao':
            return response.get('kakao_account').get('email')
        elif provider == 'google':
            return response.get('email')

    def post(self, request, provider: str) -> Response:
        # OAuth 제공 업체 이름, 요청 body의 유효성 검사
        access_code = request.data.get('code')
        if (access_code is None) or (provider not in OAUTH_PROVIDER):
            return Response(
                {
                    'detail': 'Request form is not valid',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # access code <-> access token 교환
        response = self.request_access_token(provider, access_code)
        if self.is_access_token_error(provider, response):
            return Response(
                {
                    'detail': self.get_access_token_error(provider, response)
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        access_token = self.get_access_token(provider, response)

        # OAuth 제공 업체 provider에게 email 요청
        response = self.reqeust_email(provider, access_token)
        email = self.get_email(provider, response)
        if email is None:
            return Response(
                {
                'detail': 'Email information not found'
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # OAuth 인증 email로 가입한 사용자 정보 탐색
        try:
            user = User.oauths.filter(oauth_provider=provider).get(email=email)
        except User.DoesNotExist as e:
            # 같은 email로 가입된 사용자 탐색
            # (자체 인증 모듈 또는 같은 이메일의 다른 OAuth 인증)
            try:
                User.objects.get(email=email)
            except User.DoesNotExist as e:
                # 해당 OAuth 인증을 통해 회원가입 유도
                return Response(
                    {
                        'provider': provider,
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # 같은 email로 가입된 사용자가 이미 존재한다면,
            return Response(
                {
                    'detail': 'Already registered to this email'
                },
                status=status.HTTP_403_FORBIDDEN,
            )
         
        # JWT 발급, 응답
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
        
