from django.db import models

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)      


    class Meta:
        managed = False  # No permite que Django gestione este modelo (sin migraciones ni cambios de esquema)
        db_table = 'core_country'  # Nombre de la tabla de base de datos que ya existe

    def __str__(self):
        return self.name
    

class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False  # No permite que Django gestione este modelo (sin migraciones ni cambios de esquema)
        db_table = 'core_city'  # Nombre de la tabla de base de datos que ya existe

    def __str__(self):
        return self.name
    
    
class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)      

    class Meta:
        managed = False  # No permite que Django gestione este modelo (sin migraciones ni cambios de esquema)
        db_table = 'core_language'  # Nombre de la tabla de base de datos que ya existe

    def __str__(self):
        return self.name