from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.serializers import WrapperSerializer
import yfinance as yf
from typing import Dict
from datetime import datetime


class SplitsList(APIView):
    def post(self, request):
        data = request.data
        serializer = WrapperSerializer(data=data, require_dates=False)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = serializer.validated_data
            response_data: Dict[str, dict] = {}

            for item in payload:
                ticker = item.get('ticker')
                dates = item.get('dates')

                ticker_info = yf.Ticker(ticker)
                splits = ticker_info.splits

                splits_data: Dict[str, float] = {}
                for date, value in splits.items():
                    if not dates:
                        if isinstance(date, datetime):
                            date_str = date.strftime('%Y-%m-%d')

                        splits_data[date_str] = value

                    else:
                        for date_entry in dates:
                            start_date = date_entry.get('start_date')
                            end_date = date_entry.get('end_date')

                            if (not start_date and not end_date) or (start_date <= date <= end_date):
                                if isinstance(date, datetime):
                                    date_str = date.strftime('%Y-%m-%d')

                                splits_data[date_str] = value

                response_data[ticker.rstrip('.SA')] = splits_data

            if isinstance(data, dict):
                response_data = list(response_data.values())[0]

            return Response(response_data, status=status.HTTP_200_OK)
