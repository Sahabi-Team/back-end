from rest_framework import serializers
from .models import Test

class TestSerializer(serializers.ModelSerializer):
    trainee = serializers.PrimaryKeyRelatedField(read_only=True) 
    id = serializers.IntegerField(read_only=True)  

    class Meta:
        model = Test
        fields = '__all__'  # Ensure all fields are returned
        read_only_fields = ['trainee', 'created_at']
