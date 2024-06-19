from django.urls import path
from .views import TokenObtainPair, TokenRefresh, DecodeAuth

urlpatterns = [
    path('token', TokenObtainPair.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefresh.as_view(), name='token_refresh'),
    path('untoken', DecodeAuth.as_view(), name='untoken'),
]
