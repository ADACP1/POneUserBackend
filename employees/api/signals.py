# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from employees.models import Employee

@receiver(post_save, sender=Employee)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.send_email_verification()