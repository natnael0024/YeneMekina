from datetime import timezone
import time
import requests
from rest_framework import serializers
from .models import CustomUser

import os
import dotenv
from django.http import JsonResponse
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
        username = validated_data["phone_number"]
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
        self.send_otp(phone_number)
        return user

    def send_otp(self, phone_number):
        token = os.environ.get("AFRO_API_KEY")
        user_id = os.environ.get("AFRO_USER_ID")
        url = "https://api.afromessage.com/api/challenge"
        headers = {"Authorization": "Bearer " + token}
        # import logging
        # logger = logging.getLogger(__name__)
        # logger.debug(token)
        params = {
            "from": user_id,
            "sender": "",
            "to": phone_number,
            "pr": "Verification Code",
            "ps": "",
            "sb": "4",
            "sa": "4",
            "ttl": "0",
            "len": "4",
            "t": "0",
            "callback": "",
        }
       
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            if response.status_code == 200 and data.get("acknowledge") == "success":
                # OTP sent successfully
                user = CustomUser.objects.filter(phone_number=phone_number).first()
                if user:
                    user.otp = data.get("response").get("code")
                    user.otp_timestamp = int(time.time())
                    user.save()
                else:
                    return Response(
                        {"message": "User does not exist"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:

                return Response(
                    {"message": "Unable to send OTP"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except requests.exceptions.RequestException as e:
            # Handle request exception/error
            return requests.Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



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