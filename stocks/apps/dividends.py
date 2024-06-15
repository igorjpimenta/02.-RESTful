from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.serializers import WrapperSerializer
import yfinance as yf
from typing import Dict
from datetime import datetime


class DividendsList(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = WrapperSerializer(data=data, require_dates=False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = serializer.validated_data
            response_data: Dict[str, dict] = {}

            for item in payload:
                ticker = item.get('ticker')
                ticker_info = yf.Ticker(ticker)
                dividends = ticker_info.dividends

                dividends_data: Dict[str, float] = {}
                for date, value in dividends.items():
                    if isinstance(date, datetime):
                        date = date.strftime('%Y-%m-%d')

                    dividends_data[str(date)] = value

                response_data[ticker.rstrip('.SA')] = dividends_data

            if isinstance(data, dict):
                response_data = list(response_data.values())[0]

            return Response(response_data, status=status.HTTP_200_OK)
