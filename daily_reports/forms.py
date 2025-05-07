from django import forms
from .models import DailyReportComment


class DailyReportCommentForm(forms.ModelForm):
    class Meta:
        model = DailyReportComment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee', None)
        self.daily_report = kwargs.pop('daily_report', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.employee:
            instance.employee_code = self.employee
        if self.daily_report:
            instance.daily_report_code = self.daily_report
        if commit:
            instance.save()
        return instance
