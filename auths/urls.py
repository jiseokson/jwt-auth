from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from auths.views import OAuthTokenObtainView

app_name = 'auths'

urlpatterns = [
    path('<str:provider>/token', OAuthTokenObtainView.as_view(), name='token_obtain'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
]