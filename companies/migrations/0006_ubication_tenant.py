# Generated by Django 3.2.23 on 2024-10-07 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_auto_20241001_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='ubication',
            name='tenant',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
    ]