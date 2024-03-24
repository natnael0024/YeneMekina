from rest_framework import serializers
from datetime import datetime, timedelta
from .models import DrivingLicense

class DrivingLicenseSerializer(serializers.ModelSerializer):
    is_about_to_expire = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = DrivingLicense
        fields = ['id','license_number', 'full_name', 'issue_date', 'expire_date', 'image',
                  'is_about_to_expire', 'is_expired', 'days_remaining']

    def get_is_about_to_expire(self, obj):
        current_date = datetime.now().date()
        expire_date = obj.expire_date
        if expire_date:
            days_remaining = (expire_date - current_date).days
            return days_remaining <= 30 and not self.get_is_expired(obj)
        return None

    def get_is_expired(self, obj):
        expire_date = obj.expire_date
        if expire_date:
            return expire_date < datetime.now().date()
        return None

    def get_days_remaining(self, obj):
        current_date = datetime.now().date()
        expire_date = obj.expire_date
        if expire_date:
            days_remaining = (expire_date - current_date).days
            return days_remaining if days_remaining > 0 else 0
        return None