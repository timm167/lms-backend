from rest_framework import serializers
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id')
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'role']
    
#------------------------------------------------------------#

class UserDisplaySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  
    user_id = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['user_id', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def get_user_id(self, obj):

        return obj.user.id