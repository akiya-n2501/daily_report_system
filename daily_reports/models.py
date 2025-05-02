from django.db import models
from employees.models import Employee


# Create your models here.


class DailyReport(models.Model):
    daily_report_code = models.AutoField(primary_key=True)
    employee_code = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job_description = models.TextField(max_length=2000)
    reported_on = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee_code", "reported_on"], name="uq_daily_report_01"
            )
        ]


class DailyReportComment(models.Model):
    daily_report_code = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.employee.name} {self.daily_report.reported_on} {self.comment[:7]})"
        )
