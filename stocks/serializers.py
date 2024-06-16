from rest_framework import serializers
from datetime import timedelta


class DateRangeSerializer(serializers.Serializer):
    date = serializers.DateTimeField(required=False)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)


class TickerSerializer(serializers.Serializer):
    ticker = serializers.CharField(max_length=6)
    dates = DateRangeSerializer(many=True, required=False)
    date = serializers.DateTimeField(required=False)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)

    def __init__(self, *args, **kwargs):
        self.require_dates = kwargs.pop('require_dates', True)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        if 'dates' not in data and 'date' not in data and 'start_date' not in data and 'end_date' not in data and self.require_dates:
            raise serializers.ValidationError("Either dates, or date or both start_date and end_date must be provided.")

        if 'dates' in data:
            if not data.get('dates'):
                raise serializers.ValidationError("Dates cannot be empty if provided.")

        else:
            if 'start_date' not in data and 'end_date' not in data:
                data['dates'] = [{
                    'date': data.get('date')
                }]

                data.pop('date', None)

            else:
                data['dates'] = [{
                    'start_date': data.get('start_date'),
                    'end_date': data.get('end_date')
                }]

                data.pop('start_date', None)
                data.pop('end_date', None)

        validated_dates = []

        for date_entry in data['dates']:
            date = date_entry.get('date')
            start_date = date_entry.get('start_date')
            end_date = date_entry.get('end_date')

            if not date and not start_date and not end_date and self.require_dates:
                raise serializers.ValidationError("Either date or both start_date and end_date must be provided.")

            if (start_date and not end_date) or (end_date and not start_date):
                raise serializers.ValidationError("Both start_date and end_date are required if one is provided.")

            if not start_date and not end_date:
                date_entry['start_date'] = date
                date_entry['end_date'] = date
                date_entry.pop('date', None)

            if date_entry['start_date'] and date_entry['end_date']:
                date_entry['end_date'] += timedelta(days=1)

            validated_dates.append(date_entry)

        data['dates'] = validated_dates

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
        list_serializer = ListSerializer(
            data=data,
            child=TickerSerializer(require_dates=self.require_dates)
        )

        return list_serializer.to_internal_value(data)

    def to_representation(self, instance):
        list_serializer = ListSerializer(instance=instance, many=True)  # type: ignore

        return list_serializer.data
