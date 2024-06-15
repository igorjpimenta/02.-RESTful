from rest_framework import serializers
from datetime import timedelta


class Serializer(serializers.Serializer):
    ticker = serializers.CharField(max_length=6)
    date = serializers.DateTimeField(required=False)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)

    def __init__(self, *args, **kwargs):
        self.require_dates = kwargs.pop('require_dates', True)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        date = data.get('date')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not date and not start_date and not end_date and self.require_dates:
            raise serializers.ValidationError("Either date or both start_date and end_date must be provided.")

        elif (start_date and not end_date) or (end_date and not start_date):
            raise serializers.ValidationError("Both start_date and end_date are required if one is provided.")

        if not start_date and not end_date:
            data['start_date'] = date
            data['end_date'] = date

        if self.require_dates:
            data['end_date'] += timedelta(days=1)

        return data

    def validate_ticker(self, value):
        return f"{value}.SA"


class ListSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        if isinstance(data, list):
            return super().to_internal_value(data)

        else:
            return super().to_internal_value([data])


class WrapperSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        self.require_dates = kwargs.pop('require_dates', True)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        history_list_serializer = ListSerializer(
            data=data,
            child=Serializer(require_dates=self.require_dates)
        )

        return history_list_serializer.to_internal_value(data)

    def to_representation(self, instance):
        history_list_serializer = ListSerializer(instance=instance, many=True)  # type: ignore

        return history_list_serializer.data
