from django.db import models
from companies.models import Company
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.utils import timezone
from PoneUserBackEnd.config	import URLSERVICE
#from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


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
    companies = models.ManyToManyField(Company,  blank=True , related_name='employee_companies')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True , related_name='employee_company')  
    position = models.ForeignKey(Position, on_delete=models.PROTECT, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)    
    is_manager = models.BooleanField(default=False)
    tenant = models.EmailField()
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.IntegerField(blank=True, null=True)
    city = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    origin = models.CharField(max_length=50)
    registration_date = models.DateField(auto_now_add=True)
    deleted = models.BooleanField(default=False)    
    password = models.CharField(max_length=128)
    supervisor = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='employee_supervisor')

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
        url = f'{URLSERVICE}/api/v1/employees/verifyemail/{token}'
        subjecttext = 'User Email Verification'
        message = f'Click <strong><a href="{url}">here</a></strong> to verify your email.'
        #fromemailoriginal = 'notificacionesinternas@eninter.com'
        fromemail = 'adachremail@gmail.com'
        to_email = self.email

        #send_mail(subjecttext, message, fromemailoriginal, [to_email])        

        # Configuración del correo con SendGrid
        

        email = Mail(
        from_email=fromemail,
        to_emails=to_email,
        subject=subjecttext,
        html_content = message)
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(email)
            # Verificar el código de estado de la respuesta
            if response.status_code in range(200, 300):
                print("Email sent successfully.")
            else:
                print(f"Failed to send email. Status code: {response.status_code}, Response body: {response.body}")
        except Exception as e:
            # Manejo de errores más detallado
            print(f"An error occurred: {str(e)}")
            if hasattr(e, 'body'):
                print(f"Error body: {e.body}")
            if hasattr(e, 'status_code'):
                print(f"Error status code: {e.status_code}")

class EmployeeVerificationCode(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)        

    def __str__(self):
        return self.name