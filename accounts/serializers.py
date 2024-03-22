from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser 
        fields = (
            'id', 'username', 'email', 'password', 'first_name', 'last_name',
            'phone_number', 'lang', 'avatar', 'otp', 'otp_timestamp', 'status',
             'created_at', 'updated_at'
        )
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        username = validated_data.get('phone_number')
        phone_number = validated_data['phone_number']
        if not username:
            username = phone_number
        user = CustomUser.objects.create_user(
            username=username,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'], 
            phone_number='+251' + phone_number,
            password=validated_data['password']   
        )
        return user
    
    