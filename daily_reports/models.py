# Create your models here.
from django.db import models

from employees.models import Employee


class DailyReport(models.Model):
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
=======
from django.db import models

