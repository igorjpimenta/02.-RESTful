from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.serializers import TickerListSerializer
import yfinance as yf
from typing import Dict


class LastQuote(APIView):
    def post(self, request):
        data = request.data
        serializer = TickerListSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = serializer.validated_data.get('ticker')
            response_data: Dict[str, dict] = {}

            for ticker in payload:
                ticker_info = yf.Ticker(ticker).info

                last_quote = {
                    'c': ticker_info['currentPrice'],
                    'o': ticker_info['regularMarketOpen'],
                    'h': ticker_info['regularMarketDayHigh'],
                    'l': ticker_info['regularMarketDayLow'],
                    'v': ticker_info['regularMarketVolume']
                }

                response_data[ticker.rstrip('.SA')] = last_quote

            return Response(response_data, status=status.HTTP_200_OK)
