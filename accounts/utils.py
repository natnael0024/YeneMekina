import os
import dotenv
from django.http import JsonResponse, HttpResponseServerError
from accounts.models import CustomUser
from rest_framework import status

dotenv.load_dotenv()
import requests
import time
from django.conf import settings


def send_otp(phone_number, user):
    token = os.environ.get("AFRO_API_KEY")
    user_id = os.environ.get("AFRO_USER_ID")
    url = "https://api.afromessage.com/api/challenge"
    headers = {"Authorization": "Bearer " + token}
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
     
        # timestamp = int(time.time())
        timestamp = time.time()
        if response.status_code == 200 and data.get("acknowledge") == "success":
            # OTP sent successfully
            # user = CustomUser.objects.get(phone_number=phone_number)
            user = CustomUser.objects.filter(phone_number=phone_number).latest('created_at')
            print(user)
            user.otp = data.get("response").get("code")
            user.otp_timestamp = timestamp
            user.save()
        else:
            return requests.Response(
                {"message": "Unable to send OTP"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    except requests.exceptions.RequestException as e:
        return requests.Response(
            {"message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
