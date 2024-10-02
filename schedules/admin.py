from django.contrib import admin
from schedules.models import Schedule, ScheduleDetail, ScheduleNotification  
from schedules.forms import ScheduleAdminForm
from django.core.exceptions import ValidationError

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleAdminForm
    list_display = ('id', 'name', 'tenant', 'flexible', 'flex_minutes', 'notifie', 'deleted','geolocation_required')
    ordering = ('id', 'name',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'scheduledetails':
            if hasattr(self, '_current_object') and self._current_object is not None:
                tenant = self._current_object.tenant
                kwargs['queryset'] = ScheduleDetail.objects.filter(tenant=tenant)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        self._current_object = obj
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(tenant=request.user.email)
        return qs

    def save_model(self, request, obj, form, change):
        if not change:  # Si el objeto es nuevo
            obj.tenant = request.user.email
        obj.save()

    def delete_model(self, request, obj):
        obj.delete()
    
@admin.register(ScheduleDetail)
class ScheduleDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tenant','entry_hour', 'exit_hour', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','deleted')
    ordering = ('id',)
    list_filter = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    readonly_fields = ('created_at', 'updated_at',)

@admin.register(ScheduleNotification)
class ScheduleNotificationAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    ordering = ('id','name',)
    search_fields = ('name',)
    readonly_fields = ('created_at','updated_at',)        