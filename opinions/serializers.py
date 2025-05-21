from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    ticket_id = serializers.PrimaryKeyRelatedField(source='ticket.id', read_only=True)

    class Meta:
        model = Ticket
        fields = ['ticket_id', 'title', 'name', 'text', 'phone_number', 'email', 'created_at']
        read_only_fields = ['created_at']
