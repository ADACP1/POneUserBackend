from django.contrib import admin
from .models import Clock



@admin.register(Clock)
class ClockAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'employee', 'tenant', 'longitude', 'latitude', 'type')
    search_fields = ('id', 'employee', 'tenant','type')
    ordering = ('id', 'employee',)
    

