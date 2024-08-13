from django.db import models
from companies.models import Company
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from PoneUserBackEnd.config	import URLSERVICE


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tenant = models.EmailField()   
    company = models.ManyToManyField(Company)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        
    deleted = models.BooleanField(default=False)         

    def __str__(self):
        return self.name

class Position(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tenant = models.EmailField()   
    company = models.ManyToManyField(Company)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        
    deleted = models.BooleanField(default=False)         
    
    def __str__(self):
        return self.name
    

class Employee(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)    
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)    
    email_verification_token_expires = models.DateTimeField(null=True, blank=True)        
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True,  blank=True)
    hire_date =  models.DateField(null=True,  blank=True)
    company = models.ManyToManyField(Company)
    position = models.ForeignKey(Position, on_delete=models.PROTECT, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)    
    is_manager = models.BooleanField(default=False)
    tenant = models.EmailField()
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.IntegerField()
    city = models.IntegerField()
    is_active = models.BooleanField(default=True)
    origin = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)      
    deleted = models.BooleanField(default=False)    
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def send_email_verification(self):
        token = get_random_string(length=32)
        self.email_verification_token = token
        self.email_verification_token_expires = timezone.now() + timedelta(days=10)  # Puedes ajustar el tiempo de expiración        
        self.save()

        subject = 'User Email Verification'
        message = f'Click the following link to verify your email: {URLSERVICE}/api/v1/employees/verifyemail/{token}'
        from_email = 'notificacionesinternas@eninter.com'
        to_email = self.email

        send_mail(subject, message, from_email, [to_email])                


        

class EmployeeVerificationCode(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)        

    def __str__(self):
        return self.name