from django.contrib import admin

from employees.models import Employee, Position, Department
from companies.models import Company


@admin.register(Position)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'tenant','deleted',  'created_at', 'updated_at')
    search_fields = ('id','name',)
    ordering = ('id','name',)
    readonly_fields = ('created_at','updated_at',)   

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'company':
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
        if db_field.name == 'company':
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


@admin.register(Employee)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','tenant', 'email', 'created_at','updated_at','deleted','is_manager','email_verified','origin')
    ordering = ('id','name',)
    search_fields = ('name',)
    readonly_fields = ('created_at','updated_at',)
    filter_horizontal = ('company',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'company':
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