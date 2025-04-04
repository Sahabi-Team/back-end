from rest_framework import serializers
from .models import Test

class TestSerializer(serializers.ModelSerializer):
    trainee_username = serializers.CharField(source='trainee.user.username', read_only=True)  # Show username instead of ID

    class Meta:
        model = Test
        fields = '__all__'  
        read_only_fields = ['trainee', 'created_at']  # Ensure trainee is assigned automatically
