from django.db import models
from companies.models import Company
from django.contrib.auth.models import AbstractUser



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


        

class EmployeeVerificationCode(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)        

    def __str__(self):
        return self.name
    






 
