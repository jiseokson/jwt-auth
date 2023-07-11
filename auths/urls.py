from django.urls import path

from auths.views import OAuthTokenObtainView

app_name = 'auths'

urlpatterns = [
    path('<str:provider>/token', OAuthTokenObtainView.as_view(), name='token_obtain'),
]