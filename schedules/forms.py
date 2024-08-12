from django import forms
from schedules.models import Schedule, ScheduleDetail
from django.core.exceptions import ValidationError

class ScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        tenant = cleaned_data.get('tenant')
        scheduledetails = cleaned_data.get('scheduledetails')
        if scheduledetails is not None:
            for detail in scheduledetails:
                if detail.tenant != tenant:
                    raise ValidationError("All ScheduleDetails must belong to the same tenant as the Schedule. The tenant of scheduledetail is %s" % detail.tenant)
        
        return cleaned_data