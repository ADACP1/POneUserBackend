from django.db import models


class ScheduleNotification(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name    
        

class ScheduleDetail(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    entry_hour = models.TimeField()
    exit_hour = models.TimeField()
    day_change = models.BooleanField(default=False)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tenant = models.EmailField()   
    deleted = models.BooleanField(default=False)    
    
    def __str__(self):
        return self.name    

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    flexible = models.BooleanField(null=False)
    flex_minutes = models.PositiveIntegerField(default=0)
    notifie = models.BooleanField(null=False)
    notification_ids = models.ManyToManyField(ScheduleNotification, blank=True)
    scheduledetails = models.ManyToManyField(ScheduleDetail)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tenant = models.EmailField()   
    deleted = models.BooleanField(default=False)        
        

    def __str__(self):
        return self.name