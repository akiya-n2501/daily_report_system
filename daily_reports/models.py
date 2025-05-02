from django.db import models
from employees.models import Employee


# Create your models here.
class DailyReportComment(models.Model):
    employee = models.ForeignKey("employees.Employee")
    daily_report = models.ForeignKey("DailyReport")
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.name} {self.daily_report.reported_on.date.today()} {self.comment[:7]})"
