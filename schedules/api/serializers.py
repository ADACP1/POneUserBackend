from rest_framework import serializers
from schedules.models import ScheduleNotification,ScheduleDetail,Schedule

class ScheduleNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleNotification
        fields = ['id', 'name', 'created_at', 'updated_at']



class ScheduleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleDetail
        fields = ['id', 'name', 'entry_hour', 'exit_hour', 'day_change', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'created_at', 'updated_at', 'tenant', 'deleted']



class ScheduleSerializer(serializers.ModelSerializer):
    notification_ids = ScheduleNotificationSerializer(many=True, read_only=True)
    scheduledetails = ScheduleDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'flexible', 'flex_minutes', 'notifie', 'notification_ids', 'scheduledetails', 'created_at', 'updated_at', 'tenant', 'deleted']


class ScheduleCreateUpdateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'flexible', 'flex_minutes', 'notifie', 'notification_ids', 'scheduledetails', 'created_at', 'updated_at', 'deleted']