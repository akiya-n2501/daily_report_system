from django.db import models
from employees.models import Employee


# Create your models here.


class DailyReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job_description = models.TextField(max_length=2000)
    reported_on = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Employee: {self.employee.name}, Date: {self.reported_on}, Content: {self.job_description[:7]}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "reported_on"], name="uq_daily_report_01"
            )
        ]


class DailyReportComment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Commenter: {self.employee.name}, Employee: {self.daily_report.employee.name}, Date: {self.daily_report.reported_on}, Comment: {self.comment[:7]}"
