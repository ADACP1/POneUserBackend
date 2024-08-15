from rest_framework import serializers
from schedules.models import ScheduleNotification,ScheduleDetail,Schedule

class ScheduleNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleNotification
        fields = ['id', 'name', 'created_at', 'updated_at']



class ScheduleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleDetail
        fields = ['entry_hour', 'exit_hour', 'day_change', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']



class ScheduleSerializer(serializers.ModelSerializer):
    notification_channels_ids = ScheduleNotificationSerializer(many=True, read_only=True)
    scheduledetails = ScheduleDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'flexible', 'flex_minutes', 'notifie', 'notification_channels_ids', 'scheduledetails', 'created_at', 'updated_at', 'tenant', 'deleted']


class ScheduleCreateUpdateSerializer(serializers.ModelSerializer):    
    scheduledetails = ScheduleDetailSerializer(many=True)
    notification_channels_ids = serializers.PrimaryKeyRelatedField(queryset=ScheduleNotification.objects.all(), many=True)

    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'flexible', 'flex_minutes', 'notifie', 'notification_channels_ids', 'scheduledetails']

    def create(self, validated_data):
        schedule_details_data = validated_data.pop('scheduledetails')
        notifications = validated_data.pop('notification_channels_ids')
        
        # Create Schedule instance
        schedule = Schedule.objects.create(**validated_data)
        
        # Add notifications to Schedule
        schedule.notification_channels_ids.set(notifications)
        
        # Create and add ScheduleDetail instances to Schedule
        for detail_data in schedule_details_data:
            # You should ensure tenant is handled properly
            schedule_detail = ScheduleDetail.objects.create(**detail_data, tenant=schedule.tenant)
            schedule.scheduledetails.add(schedule_detail)
        
        return schedule
    """
    notification_ids = ScheduleNotificationSerializer(many=True, read_only=True)
    scheduledetails = ScheduleDetailSerializer(many=True, read_only=True)    
    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'flexible', 'flex_minutes', 'notifie', 'notification_ids', 'scheduledetails']
    """