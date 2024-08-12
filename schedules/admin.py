from django.contrib import admin
from schedules.models import Schedule, ScheduleDetail, ScheduleNotification  
from schedules.forms import ScheduleAdminForm
from django.core.exceptions import ValidationError

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleAdminForm
    list_display = ('id', 'name', 'tenant', 'flexible', 'flex_minutes', 'notifie', 'deleted')
    ordering = ('id', 'name',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'scheduledetails':
            # Filtra ScheduleDetail por tenant en base al tenant del Schedule
            if request._obj_ is not None:
                tenant = request._obj_.tenant
                kwargs['queryset'] = ScheduleDetail.objects.filter(tenant=tenant)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


    def get_form(self, request, obj=None, **kwargs):
        # Guardar el objeto en la request para usarlo en formfield_for_manytomany
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)

    
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