from django.db import models


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.EmailField()   
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)   
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.IntegerField()
    city = models.IntegerField() 
    website = models.URLField(blank=True, null=True)
    vat_number = models.CharField(max_length=20, blank=True, null=True)
    registration_number = models.CharField(max_length=50, blank=True, null=True)
    employee_count = models.IntegerField(blank=True, null=True)
    founding_date = models.DateField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    logo = models.FileField(upload_to='company_logos/', blank=True, null=True)        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)      
    deleted = models.BooleanField(default=False)     

    def __str__(self):
        return self.name