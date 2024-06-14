from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.serializers import SplitsSerializer
import yfinance as yf


class SplitsList(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SplitsSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = serializer.validated_data
            ticker = yf.Ticker(payload.get('ticker'))
            splits = ticker.splits

            splits_response = {}
            for date, value in splits.items():
                date = date.strftime('%Y-%m-%d')
                splits_response[date] = value

            return Response(splits_response, status=status.HTTP_200_OK)
