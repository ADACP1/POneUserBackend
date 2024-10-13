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
        fields = ['id', 'name', 'description', 'flexible', 'flex_minutes', 'notifie', 'notification_channels_ids', 'scheduledetails','geolocation_required', 'created_at', 'updated_at', 'tenant', 'deleted']


class ScheduleCreateUpdateSerializer(serializers.ModelSerializer):
    scheduledetails = ScheduleDetailSerializer(many=True)
    notification_channels_ids = serializers.PrimaryKeyRelatedField(queryset=ScheduleNotification.objects.all(), many=True)

    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'flexible', 'flex_minutes', 'notifie', 'notification_channels_ids', 'scheduledetails', 'geolocation_required']

    def update(self, instance, validated_data):
        tenantinfo = instance.tenant
        # Actualiza los campos del modelo Schedule
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.flexible = validated_data.get('flexible', instance.flexible)
        instance.flex_minutes = validated_data.get('flex_minutes', instance.flex_minutes)
        instance.notifie = validated_data.get('notifie', instance.notifie)
        instance.geolocation_required = validated_data.get('geolocation_required', instance.geolocation_required)
        instance.save()

        # Eliminar los detalles existentes
        instance.scheduledetails.all().delete()

        # Crear nuevos ScheduleDetails a partir de los datos validados
        
        details_data = validated_data.get('scheduledetails', [])
        for detail_data in details_data:
            schedule_detail = ScheduleDetail.objects.create(schedule=instance,tenant = tenantinfo,name =instance.name+' '+str(instance.id), **detail_data)
            instance.scheduledetails.add(schedule_detail)


        # Actualizar las notificaciones
        notification_ids = validated_data.get('notification_channels_ids', [])
        instance.notification_channels_ids.set(notification_ids)

        return instance

    def create(self, validated_data):

        request = self.context.get('request')
        tenantinfo = request.user.tenant 
        schedule_details_data = validated_data.pop('scheduledetails')
        notifications = validated_data.pop('notification_channels_ids')
        
        # Create Schedule instance
        schedule = Schedule.objects.create(**validated_data)
        
        # Add notifications to Schedule
        schedule.notification_channels_ids.set(notifications)
        
        # Create and add ScheduleDetail instances to Schedule
        for detail_data in schedule_details_data:
            schedule_detail = ScheduleDetail.objects.create(schedule=schedule,tenant = tenantinfo,name =schedule.name+' '+str(schedule.id), **detail_data)
            schedule.scheduledetails.add(schedule_detail)
        
        return schedule
    """
    notification_ids = ScheduleNotificationSerializer(many=True, read_only=True)
    scheduledetails = ScheduleDetailSerializer(many=True, read_only=True)    
    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'flexible', 'flex_minutes', 'notifie', 'notification_ids', 'scheduledetails']
    """