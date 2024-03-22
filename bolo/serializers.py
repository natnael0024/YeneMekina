from rest_framework import serializers
from .models import Bolo
from vehicle.models import Vehicle
from datetime import datetime, timedelta
from datetime import datetime


class BoloSerializer(serializers.ModelSerializer):
    isAboutToExpire = serializers.SerializerMethodField()
    isExpired = serializers.SerializerMethodField()
    daysRemaining = serializers.SerializerMethodField()
    plate_number = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Bolo
        fields = ('id', 'inspection_date', 'expire_date', 'image','vehicle_id', 'isAboutToExpire', 'isExpired', 'daysRemaining', 'plate_number', 'completed')


    def get_isAboutToExpire(self, obj):
        if obj.expire_date:
            current_date = datetime.now().date()
            expire_date = obj.expire_date

            if isinstance(expire_date, str):
                expire_date = datetime.strptime(expire_date, '%Y-%m-%d').date()

            day_diff = (expire_date - current_date).days
            return day_diff <= 30 and not expire_date < current_date
        return None


    def get_isExpired(self, obj):
        if obj.expire_date:
            current_date = datetime.now().date()
            expire_date = obj.expire_date

            if isinstance(expire_date, str):
                expire_date = datetime.strptime(expire_date, '%Y-%m-%d').date()

            return expire_date < current_date
        return None

    def get_daysRemaining(self, obj):
        if obj.expire_date:
            current_date = datetime.now().date()
            expire_date = obj.expire_date

            if isinstance(expire_date, str):
                expire_date = datetime.strptime(expire_date, '%Y-%m-%d').date()

            if expire_date < current_date:
                return 0
            return (expire_date - current_date).days
        return None

    def get_plate_number(self, obj):
        vehicle = Vehicle.objects.filter(id=obj.vehicle_id).first()
        if vehicle:
            return vehicle.plate_number
        return None

    def get_completed(self, obj):
        return "completed" if obj.inspection_date and obj.expire_date else "incomplete"