# Generated by Django 3.2.23 on 2024-08-10 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='city',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='country',
        ),
    ]