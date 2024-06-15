from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.serializers import WrapperSerializer
import yfinance as yf
from typing import Dict
from datetime import datetime


class HistoryData(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = WrapperSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = serializer.validated_data
            response_data: Dict[str, dict] = {}

            for item in payload:
                ticker = item.get('ticker')
                ticker_info = yf.Ticker(ticker)
                history = ticker_info.history(
                    start=item.get('start_date'),
                    end=item.get('end_date')
                )

                history_data: Dict[str, dict] = {}
                for date, row in history.iterrows():
                    if isinstance(date, datetime):
                        date = date.strftime('%Y-%m-%d')

                    history_data[str(date)] = {
                        "o": row['Open'],
                        "h": row['High'],
                        "l": row['Low'],
                        "c": row['Close'],
                        "v": row['Volume'],
                    }

                response_data[ticker.rstrip('.SA')] = history_data

            if isinstance(data, dict):
                response_data = list(response_data.values())[0]

            return Response(response_data, status=status.HTTP_200_OK)
