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
    
    
    # def clean_job_description(self):
    #      job_description = self.cleaned_data.get("job_description")
    #      if len(job_description) > 2000:
    #         raise forms.ValidationError("業務内容は2000文字以内で入力してください。")
    #      return job_description


    def save(self, commit=True):
        daily_report = super().save(commit=False)
        if commit:
            daily_report.save()
        return daily_report