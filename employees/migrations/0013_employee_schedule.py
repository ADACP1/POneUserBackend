# Generated by Django 3.2.23 on 2024-09-25 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0004_alter_scheduledetail_name'),
        ('employees', '0012_employee_preferred_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='employee_schedule', to='schedules.schedule'),
        ),
    ]