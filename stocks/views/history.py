from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.serializers import InfoSerializer
import yfinance as yf
from typing import Dict
from datetime import datetime


class HistoryData(APIView):
    def post(self, request):
        data = request.data

        if not isinstance(data, list):
            data = [data]

        serializer = InfoSerializer(data=data, many=True, require_dates=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = serializer.validated_data
            response_data: Dict[str, dict] = {}

            for item in payload:
                ticker = item.get('ticker')
                ticker_info = yf.Ticker(ticker)
                splits = ticker_info.splits
                dates = item.get('dates')

                history_data: Dict[str, dict] = response_data.get(ticker.rstrip('.SA'), {})
                for date_entry in dates:
                    history = ticker_info.history(
                        start=date_entry.get('start_date'),
                        end=date_entry.get('end_date'),
                        auto_adjust=False
                    )

                    for date, row in history.iterrows():
                        split_coefficient = splits[splits.index >= date].product()

                        if isinstance(date, datetime):
                            date = date.strftime('%Y-%m-%d')

                        history_data[str(date)] = {
                            "o": row['Open'] * split_coefficient,
                            "h": row['High'] * split_coefficient,
                            "l": row['Low'] * split_coefficient,
                            "c": row['Close'] * split_coefficient,
                            "v": row['Volume'] * split_coefficient,
                        }

                response_data[ticker.rstrip('.SA')] = history_data

            if isinstance(data, dict):
                response_data = list(response_data.values())[0]

            return Response(response_data, status=status.HTTP_200_OK)
