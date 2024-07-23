from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Test(APIView):
    def get(self, request):
        response_data = {
            "status": "successful"
        }

        return Response(response_data, status=status.HTTP_200_OK)
