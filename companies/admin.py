# admin.py
from django.contrib import admin
from .models import Company, Ubication



@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tenant', 'email', 'deleted', 'created_at', 'updated_at')
    search_fields = ('id', 'name', 'email')
    ordering = ('id', 'name',)
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(Ubication)
class UbicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tenant','company','longitude', 'latitude', 'deleted')
    search_fields = ('id', 'name')
    ordering = ('id', 'name',)
    readonly_fields = ('created_at', 'updated_at',)
