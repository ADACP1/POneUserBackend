# Generated by Django 3.2.23 on 2024-08-13 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_alter_company_tenant'),
        ('employees', '0006_alter_employee_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='companies',
            field=models.ManyToManyField(blank=True, related_name='employee_companies', to='companies.Company'),
        ),
        migrations.RemoveField(
            model_name='employee',
            name='company',
        ),
        migrations.AddField(
            model_name='employee',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='employee_company', to='companies.company'),
        ),
    ]
