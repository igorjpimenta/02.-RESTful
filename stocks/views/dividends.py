from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.serializers import DividendsSerializer
import yfinance as yf


class DividendsList(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = DividendsSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = serializer.validated_data
            ticker = yf.Ticker(payload.get('ticker'))
            dividends = ticker.dividends

            dividends_response = {}
            for date, value in dividends.items():
                date = date.strftime('%Y-%m-%d')
                dividends_response[date] = value

            return Response(dividends_response, status=status.HTTP_200_OK)
