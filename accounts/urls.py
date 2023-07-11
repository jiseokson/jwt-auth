from django.urls import path

from accounts.views import AccountsInfo

app_name = 'accounts'

urlpatterns = [
    path('', AccountsInfo.as_view(), name='info'),
]