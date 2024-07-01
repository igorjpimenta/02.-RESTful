from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.serializers import InfoSerializer
from stocks.scrappers import StockTicker
from typing import Dict
from datetime import datetime


class BonusesList(APIView):
    def post(self, request):
        data = request.data

        if not isinstance(data, list):
            data = [data]

        serializer = InfoSerializer(data=data, many=True, require_dates=False)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = serializer.validated_data
            response_data: Dict[str, dict] = {}

            for item in payload:
                ticker = item.get('ticker')
                dates = item.get('dates')
                application_category = item.get('application_category')

                bonuses_data: Dict[str, float] = {}
                if application_category == 'stock':
                    st = StockTicker(ticker.rstrip('.SA'))
                    bonuses = st.get_bonuses()
                    bonuses = bonuses.set_index('exercised_on')['ratio']

                for date, value in bonuses.items():
                    if not dates:
                        if isinstance(date, datetime):
                            date_str = date.strftime('%Y-%m-%d')

                        bonuses_data[date_str] = value

                    else:
                        for date_entry in dates:
                            start_date = date_entry.get('start_date')
                            end_date = date_entry.get('end_date')

                            if (not start_date and not end_date) or (start_date <= date <= end_date):
                                if isinstance(date, datetime):
                                    date_str = date.strftime('%Y-%m-%d')

                                bonuses_data[date_str] = value

                response_data[ticker.rstrip('.SA')] = bonuses_data

            if isinstance(data, dict):
                response_data = list(response_data.values())[0]

            return Response(response_data, status=status.HTTP_200_OK)
