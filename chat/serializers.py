from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    fromMe = serializers.SerializerMethodField()
    text = serializers.CharField(source='content')
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    seen = serializers.BooleanField()

    class Meta:
        model = Message
        fields = ['fromMe', 'text', 'date', 'time', 'seen']

    def get_fromMe(self, obj):
        request = self.context.get('request')
        return obj.sender == request.user

    def get_date(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d')

    def get_time(self, obj):
        return obj.timestamp.strftime('%H:%M:%S')
