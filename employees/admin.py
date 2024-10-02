
from django.contrib import admin

from employees.models import Employee, Position, Department
from companies.models import Company
from django.contrib.auth.admin import UserAdmin as BaseTenantAdmin





@admin.register(Employee)
class EmployeeAdmin(BaseTenantAdmin):   
    #pass
    list_display = (
        'id','email', 'username', 'name', 'tenant', 'is_manager', 'is_active', 'email_verified'
    )
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('name', 'last_name', 'phone_number', 'date_of_birth', 'hire_date')}),
        ('Company Info', {'fields': ('companies', 'company','ubication')}),
        ('Position & Department', {'fields': ('position', 'department')}),
        ('Address Info', {'fields': ('address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country')}),
        ('Verification Info', {'fields': ('email_verified', 'email_verification_token', 'email_verification_token_expires')}),
        ('Additional Info', {'fields': ('tenant', 'origin', 'is_manager','supervisor')}),
        ('Status & Dates', {'fields': ('is_active', 'deleted')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),        
    )

    readonly_fields = ('get_registration_date','id')
    def get_registration_date(self, obj):
        return obj.registration_date.strftime('%Y-%m-%d')

    get_registration_date.short_description = 'Registration Date'

    filter_horizontal = ('companies',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'companies':
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                try:
                    employee = Employee.objects.get(pk=obj_id)
                    kwargs['queryset'] = Company.objects.filter(tenant=employee.tenant)
                except Employee.DoesNotExist:
                    kwargs['queryset'] = Company.objects.none()
            else:
                kwargs['queryset'] = Company.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'supervisor':
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                try:
                    employee = Employee.objects.get(pk=obj_id)
                    # Filtrar solo los empleados que pertenecen al mismo tenant
                    kwargs['queryset'] = Employee.objects.filter(tenant=employee.tenant)
                except Employee.DoesNotExist:
                    kwargs['queryset'] = Employee.objects.none()
            else:
                kwargs['queryset'] = Employee.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)    







@admin.register(Position)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'tenant','deleted',  'created_at', 'updated_at')
    search_fields = ('id','name',)
    ordering = ('id','name',)
    readonly_fields = ('created_at','updated_at',)   

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'companies':
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                try:
                    position = Position.objects.get(pk=obj_id)
                    kwargs['queryset'] = Company.objects.filter(tenant=position.tenant)
                except Position.DoesNotExist:
                    kwargs['queryset'] = Company.objects.none()
            else:
                kwargs['queryset'] = Position.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)        


@admin.register(Department)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'tenant', 'deleted', 'created_at', 'updated_at')
    search_fields = ('id','name',)
    ordering = ('id','name',)
    readonly_fields = ('created_at','updated_at',)   

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'companies':
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                try:
                    department = Department.objects.get(pk=obj_id)
                    kwargs['queryset'] = Company.objects.filter(tenant=department.tenant)
                except Department.DoesNotExist:
                    kwargs['queryset'] = Company.objects.none()
            else:
                kwargs['queryset'] = Department.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)    