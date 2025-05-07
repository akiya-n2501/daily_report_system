from django.contrib import admin

# Register your models here.
from .models import DailyReport, DailyReportComment

admin.site.register(DailyReport)
admin.site.register(DailyReportComment)
