from django.contrib import admin

from core.models import Country, Language, City
"""

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id','name','created_at','updated_at',)
    ordering = ('id','name',)
    search_fields = ('name',)
    readonly_fields = ('created_at','updated_at',)      

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id','name','created_at','updated_at','country')
    ordering = ('id','name',)
    search_fields = ('name',)
    readonly_fields = ('created_at','updated_at',)          

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id','name','created_at','updated_at',)
    ordering = ('id','name',)
    search_fields = ('name',)
    readonly_fields = ('created_at','updated_at',)          
    """