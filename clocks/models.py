from django.db import models
from employees.models import Employee
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