# Generated by Django 3.2.23 on 2024-08-13 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_auto_20240813_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='city',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='country',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
