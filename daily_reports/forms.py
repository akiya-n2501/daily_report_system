from django import forms

from .models import DailyReport


class DailyReportForm(forms.ModelForm):

    class Meta:
        model = DailyReport
        fields = ["employee_code","job_description","reported_on"]
        labels = {"employee_code": "名前",
                  "job_description": "業務内容",
                  "reported_on": "日付",
                  }

    def save(self, commit=True):
        daily_report = super().save(commit=False)
        if commit:
            daily_report.save()
        return daily_report