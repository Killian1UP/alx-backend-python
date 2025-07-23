import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')
    sender_id = django_filters.UUIDFilter(field_name="sender_id__user_id")  # if using UUID as PK

    class Meta:
        model = Message
        fields = ['sender_id', 'conversation', 'start_date', 'end_date']
