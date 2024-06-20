from rest_framework.serializers import Serializer, ListField, CharField, DateTimeField, ValidationError
from datetime import timedelta


class DateRangeSerializer(Serializer):
    date = DateTimeField(required=False)
    start_date = DateTimeField(required=False)
    end_date = DateTimeField(required=False)


class TickerListSerializer(Serializer):
    ticker = ListField(
        child=CharField(max_length=6)
    )

    def validate_ticker(self, value):
        if not value:
            raise ValidationError("'ticker' cannot be an empty list.")

        return [f"{item}.SA" for item in value]


class InfoSerializer(Serializer):
    ticker = CharField(max_length=6)
    dates = DateRangeSerializer(many=True, required=False)
    date = DateTimeField(required=False)
    start_date = DateTimeField(required=False)
    end_date = DateTimeField(required=False)

    def __init__(self, *args, **kwargs):
        self.require_dates = kwargs.pop('require_dates', True)
        super().__init__(*args, **kwargs)

    def validate_ticker(self, value):
        return f"{value}.SA"

    def validate(self, data):
        missing_fields = (
            'dates' not in data and
            'date' not in data and
            'start_date' not in data and
            'end_date' not in data
        )

        if missing_fields and self.require_dates:
            raise ValidationError("Either 'dates', or 'date' or both 'start_date' and 'end_date' must be provided.")

        if 'dates' in data:
            if not data.get('dates') and self.require_dates:
                raise ValidationError("'dates' must be an array containing 'date' or both 'start_date' and 'end_date'.")

        elif not missing_fields:
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

        if not missing_fields:
            for date_entry in data['dates']:
                date = date_entry.get('date')
                start_date = date_entry.get('start_date')
                end_date = date_entry.get('end_date')

                if not date and not start_date and not end_date:
                    if self.require_dates:
                        raise ValidationError("Either 'date' or both 'start_date' and 'end_date' must be provided.")

                else:
                    if (start_date and not end_date) or (end_date and not start_date):
                        raise ValidationError("Both 'start_date' and 'end_date' are required if one is provided.")

                    if not start_date and not end_date:
                        date_entry['start_date'] = date
                        date_entry['end_date'] = date
                        date_entry.pop('date', None)

                    if date_entry['start_date'] and date_entry['end_date']:
                        date_entry['end_date'] += timedelta(days=1)

                    validated_dates.append(date_entry)

        data['dates'] = validated_dates

        return data
