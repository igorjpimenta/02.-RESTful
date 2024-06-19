import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
from django.conf import settings
from .serializers import UserLoginSerializer, TokenRefreshSerializer


class TokenObtainPair(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token  # type: ignore

        return Response({
            'refresh': str(refresh),
            'refresh_exp': str(refresh.payload['exp']),
            'access': str(access_token),
            'access_exp': str(access_token.payload['exp']),
        })


class TokenRefresh(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        return Response(data)


class DecodeAuth(APIView):
    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', '').split(' ')[1]

        try:
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            return Response(decoded_payload, status=status.HTTP_200_OK)

        except (InvalidToken, TokenError, jwt.ExpiredSignatureError, jwt.DecodeError) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
