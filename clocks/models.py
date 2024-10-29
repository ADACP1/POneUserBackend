from django.db import models
from employees.models import Employee
from companies.models import Company


class AbsenceType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tenant = models.EmailField()   
    companies = models.ManyToManyField(Company)
    require_validation = models.BooleanField(default=False)
    require_addittional_info = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        
    deleted = models.BooleanField(default=False)         

    def __str__(self):
        return self.name
    


class AbsenceEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    tenant = models.EmailField()   
    absence_type = models.ForeignKey(AbsenceType, on_delete=models.PROTECT)
    text = models.TextField()
    validate = models.BooleanField(default=False)
    filepath = models.FileField(upload_to='absences/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        
    deleted = models.BooleanField(default=False)         


# Create your models here.
class Clock(models.Model):
    TYPE_CHOICES = [
        ('in', 'Clock In'),
        ('out', 'Clock Out'),
    ]

    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)  # Guarda la fecha y hora del fichaje automáticamente
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)  # Relación con el usuario empleado
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Longitud GPS
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Latitud GPS
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)  # Entrada o salida
    tenant = models.EmailField()  # Correo del tenant (inquilino, empresa)

    def __str__(self):
        return f"{self.employee.username} - {self.date} ({self.get_type_display()})"