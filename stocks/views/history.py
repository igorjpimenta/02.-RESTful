from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.serializers import HistorySerializer
import yfinance as yf


class HistoryData(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = HistorySerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = serializer.validated_data
            ticker = yf.Ticker(payload.get('ticker'))
            history = ticker.history(
                start=payload.get('start_date'),
                end=payload.get('end_date')
            )

            history_response = {}
            for date, row in history.iterrows():
                history_response[date.strftime('%Y-%m-%d')] = {
                    "Open": row['Open'],
                    "High": row['High'],
                    "Low": row['Low'],
                    "Close": row['Close'],
                    "Volume": row['Volume'],
                }

            return Response(history_response, status=status.HTTP_200_OK)
