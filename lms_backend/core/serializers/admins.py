from core.models import Admin
from rest_framework import serializers

class AdminSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    id = serializers.IntegerField(source='user.id')

    class Meta:
        model = Admin
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff']

#------------------------------------------------------------#


