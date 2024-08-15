from django import forms
from schedules.models import Schedule, ScheduleDetail
from django.core.exceptions import ValidationError

class ScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        tenant = self.instance.tenant
        scheduledetails = cleaned_data.get('scheduledetails')

        if scheduledetails:
            for detail in scheduledetails.all():  # .all() para trabajar con queryset
                if detail.tenant != tenant:
                    raise ValidationError(
                        "All ScheduleDetails must belong to the same tenant as the Schedule. The tenant of schedule detail is %s" % detail.tenant
                    )
        return cleaned_data