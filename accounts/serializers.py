
import time
import requests
from rest_framework import serializers

from accounts.utils import send_otp
from .models import CustomUser
import os
import dotenv
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

dotenv.load_dotenv()

from django.contrib.auth.models import Group

class UserSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)
    class Meta:
        model = CustomUser 
       
        fields = (
            'id', 'username', 'email', 'password', 'first_name', 'last_name',
            'phone_number', 'lang', 'avatar', 'otp', 'otp_timestamp', 'status',
             'created_at', 'updated_at','group'
        )
        extra_kwargs = {"password": {"write_only": True}}
    def create(self, validated_data):
        username = validated_data["username"]
        phone_number = validated_data["phone_number"]
        if not username:
            username = phone_number
        user = CustomUser.objects.create_user(
            username=username,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number="+251" + phone_number,
            password=validated_data["password"],
            avatar=validated_data["avatar"],
        )
        return user
    
     
  
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance
