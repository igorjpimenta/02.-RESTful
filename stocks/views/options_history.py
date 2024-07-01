from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.serializers import OptionsSerializer
from stocks.scrappers import StockOptions
from typing import Dict
from datetime import datetime


class OptionsHistoryData(APIView):
    def post(self, request):
        data = request.data

        if not isinstance(data, list):
            data = [data]

        serializer = OptionsSerializer(data=data, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = serializer.validated_data
            response_data: Dict[str, dict] = {}

            for item in payload:
                cod = item.get('cod')
                dates = item.get('dates')

                so = StockOptions(cod)
                history = so.get_history()

                history_data: Dict[str, dict] = {}
                for date, row in history.iterrows():
                    for date_entry in dates:
                        start_date = date_entry.get('start_date')
                        end_date = date_entry.get('end_date')

                        if (not start_date and not end_date) or (start_date <= date <= end_date):
                            if isinstance(date, datetime):
                                date_str = date.strftime('%Y-%m-%d')

                            history_data[date_str] = {
                                "o": row['Open'],
                                "h": row['High'],
                                "l": row['Low'],
                                "c": row['Close'],
                                "v": row['Volume'],
                            }

                response_data[cod] = history_data

            if isinstance(data, dict):
                response_data = list(response_data.values())[0]

            return Response(response_data, status=status.HTTP_200_OK)
