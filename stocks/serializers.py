from rest_framework import serializers


class HistorySerializer(serializers.Serializer):
    ticker = serializers.CharField(max_length=6)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField(required=False)

    def validate_ticker(self, value):
        return f"{value}.SA"


class DividendsSerializer(serializers.Serializer):
    ticker = serializers.CharField(max_length=6)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)

    def validate_ticker(self, value):
        return f"{value}.SA"


class SplitsSerializer(serializers.Serializer):
    ticker = serializers.CharField(max_length=6)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)

    def validate_ticker(self, value):
        return f"{value}.SA"
