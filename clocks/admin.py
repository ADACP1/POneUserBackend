from django.contrib import admin
from .models import Clock, AbsenceType



@admin.register(Clock)
class ClockAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'employee', 'tenant', 'longitude', 'latitude', 'type')
    search_fields = ('id', 'employee', 'tenant','type')
    ordering = ('id', 'employee',)
    

@admin.register(AbsenceType)
class AbsenceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tenant', 'require_validation', 'require_addittional_info')
    search_fields = ('id', 'name', 'tenant')
    ordering = ('id', 'name',)
